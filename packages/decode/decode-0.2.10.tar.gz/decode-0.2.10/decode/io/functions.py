# coding: utf-8

# public items
__all__ = [
    'loaddfits',
    'savefits',
    'loadnetcdf',
    'savenetcdf',
]

# standard library
from logging import getLogger

# dependent packages
import decode as dc
import numpy as np
import xarray as xr
from astropy.io import fits
from scipy.interpolate import interp1d


def loaddfits(fitsname, coordtype='azel', loadtype='temperature', starttime=None, endtime=None,
              pixelids=None, scantype=None, mode=0, **kwargs):
    """Load a decode array from a DFITS file.

    Args:
        fitsname (str): Name of DFITS file.
        coordtype (str): Coordinate type included into a decode array, azel or radec.
        loadtype (str): Data format of xarray.
            'Tsignal': Temperature
            'Psignal': Power
        starttime (int, str or numpy.datetime64): Start time of loaded data.
            It can be specified by the start index (int), the time compatible with numpy.datetime64 (str),
            or numpy.datetime64 (numpy.datetime64). Default is None and it means the data will be loaded
            from the first record.
        endtime (int, str or numpy.datetime64): End time of loaded data.
            It can be specified by the end index (int), the time compatible with numpy.datetime64 (str),
            or numpy.datetime64 (numpy.datetime64). Default is None and it means the data will be loaded
            until the last record.
        pixelids (int or list): Under development.
        scantype (str): Under development.
        mode (int):
            0: Relative coordinates with cosine projection (RECOMMENDED).
            1: Relative coordinates without cosine projection.
            2: Absolute coordinates.

    Returns:
        decode array (decode.array): Loaded decode array.
    """
    if mode in [0, 1, 2]:
        logger = getLogger('decode.io.loaddfits (mode={})'.format(mode))
    else:
        raise KeyError(mode)

    ### open hdulist
    hdulist = fits.open(fitsname)

    ### load data
    obsinfo = hdulist['OBSINFO'].data
    obshdr  = hdulist['OBSINFO'].header
    antlog  = hdulist['ANTENNA'].data
    readout = hdulist['READOUT'].data
    wealog  = hdulist['WEATHER'].data

    ### obsinfo
    masterids = obsinfo['masterids'][0].astype(np.int64)
    kidids    = obsinfo['kidids'][0].astype(np.int64)
    kidfreqs  = obsinfo['kidfreqs'][0].astype(np.float64)
    kidtypes  = obsinfo['kidtypes'][0].astype(np.int64)

    ### parse start/end time
    t_ant = np.array(antlog['time']).astype(np.datetime64)
    t_out = np.array(readout['starttime']).astype(np.datetime64)
    t_wea = np.array(wealog['time']).astype(np.datetime64)

    if starttime is None:
        startindex = 0
    elif isinstance(starttime, int):
        startindex = starttime
    elif isinstance(starttime, str):
        startindex = np.searchsorted(t_out, np.datetime64(starttime))
    elif isinstance(starttime, np.datetime64):
        startindex = np.searchsorted(t_out, starttime)
    else:
        raise ValueError(starttime)

    if endtime is None:
        endindex = t_out.shape[0]
    elif isinstance(endtime, int):
        endindex = endtime
    elif isinstance(endtime, str):
        endindex = np.searchsorted(t_out, np.datetime64(endtime), 'right')
    elif isinstance(endtime, np.datetime64):
        endindex = np.searchsorted(t_out, endtime, 'right')
    else:
        raise ValueError(starttime)

    if t_out[endindex-1] > t_ant[-1]:
        logger.warning('Endtime of readout is adjusted to that of ANTENNA HDU.')
        endindex = np.searchsorted(t_out, t_ant[-1], 'right')

    logger.debug('startindex: {}'.format(startindex))
    logger.debug('endindex: {}'.format(endindex))
    t_out = t_out[startindex:endindex]

    ### readout
    pixelid = readout['pixelid'][startindex:endindex]
    if loadtype == 'temperature':
        response = readout['Tsignal'][startindex:endindex].astype(np.float64)
    elif loadtype == 'power':
        response = readout['Psignal'][startindex:endindex].astype(np.float64)

    ### antenna
    if coordtype == 'azel':
        x    = antlog['az'].copy()
        y    = antlog['el'].copy()
        xref = np.median(antlog['az_center'])
        yref = np.median(antlog['el_center'])
        if mode in [0, 1]:
            x -= antlog['az_center']
            y -= antlog['el_center']
            if mode == 0:
                x *= np.cos(np.deg2rad(antlog['el']))
    elif coordtype == 'radec':
        x    = antlog['ra'].copy()
        y    = antlog['dec'].copy()
        xref = obshdr['RA']
        yref = obshdr['DEC']
        if mode in [0, 1]:
            x -= xref
            y -= yref
            if mode == 0:
                x *= np.cos(np.deg2rad(antlog['dec']))
    scantype = antlog['scantype']

    ### weatherlog
    temp      = wealog['temperature']
    pressure  = wealog['pressure']
    vpressure = wealog['vapor-pressure']
    windspd   = wealog['windspd']
    winddir   = wealog['winddir']

    ### interpolation
    dt_out  = (t_out - t_out[0]).astype(np.float64)
    dt_ant  = (t_ant - t_out[0]).astype(np.float64)
    dt_wea  = (t_wea - t_out[0]).astype(np.float64)
    x_i     = np.interp(dt_out, dt_ant, x)
    y_i     = np.interp(dt_out, dt_ant, y)

    temp_i       = np.interp(dt_out, dt_wea, temp)
    pressure_i   = np.interp(dt_out, dt_wea, pressure)
    vpressure_i  = np.interp(dt_out, dt_wea, vpressure)
    windspd_i    = np.interp(dt_out, dt_wea, windspd)
    winddir_i    = np.interp(dt_out, dt_wea, winddir)

    scandict     = {t: n for n, t in enumerate(np.unique(scantype))}
    scantype_v   = np.zeros(scantype.shape[0], dtype=int)
    for k, v in scandict.items():
        scantype_v[scantype == k] = v
    scantype_vi  = interp1d(dt_ant, scantype_v, kind='nearest', bounds_error=False,
                            fill_value=(scantype_v[0], scantype_v[-1]))(dt_out)
    scantype_i   = np.full_like(scantype_vi, 'GRAD', dtype='<U8')
    for k, v in scandict.items():
        scantype_i[scantype_vi == v] = k

    ### coordinates
    tcoords      = {'x': x_i, 'y': y_i, 'time': t_out, 'temp': temp_i, 'pressure': pressure_i,
                    'vapor-pressure': vpressure_i, 'windspd': windspd_i, 'winddir': winddir_i,
                    'scantype': scantype_i}
    chcoords     = {'masterid': masterids, 'kidid': kidids, 'kidfq': kidfreqs, 'kidtp': kidtypes}
    scalarcoords = {'coordsys': coordtype.upper(), 'datatype': loadtype, 'xref': xref, 'yref': yref}

    ### make array
    array = dc.array(response, tcoords=tcoords, chcoords=chcoords, scalarcoords=scalarcoords)

    ### close hdu
    hdulist.close()

    return array


def savefits(dataarray, fitsname, **kwargs):
    """Save a dataarray to a 3D-cube FITS file.

    Args:
        dataarray (xarray.DataArray): Dataarray to be saved.
        fitsname (str): Name of output FITS file.
        kwargs (optional): Other arguments common with astropy.io.fits.writeto().
    """
    if dataarray.type == 'dca':
        pass
    elif dataarray.type == 'dcc':
        xr.DataArray.dcc.savefits(dataarray, fitsname, **kwargs)
    elif dataarray.type == 'dcs':
        pass
    else:
        pass


def loadnetcdf(filename, copy=True):
    """Load a dataarray from a NetCDF file.

    Args:
        filename (str): Filename (*.nc).
        copy (bool): If True, dataarray is copied in memory. Default is True.

    Returns:
        dataarray (xarray.DataArray): Loaded dataarray.
    """
    if copy:
        dataarray = xr.open_dataarray(filename).copy()
    else:
        dataarray = xr.open_dataarray(filename)

    if dataarray.name is None:
        dataarray.name = filename.rstrip('.nc')

    for key, val in dataarray.coords.items():
        if val.dtype.kind == 'S':
            dataarray[key] = val.astype('U')
        elif val.dtype == np.int32:
            dataarray[key] = val.astype('i8')

    return dataarray


def savenetcdf(dataarray, filename=None):
    """Save a dataarray to a NetCDF file.

    Args:
        dataarray (xarray.DataArray): Dataarray to be saved.
        filename (str): Filename (used as <filename>.nc).
            If not spacified, random 8-character name will be used.
    """
    if filename is None:
        if dataarray.name is not None:
            filename = dataarray.name
        else:
            filename = uuid4().hex[:8]

    if not filename.endswith('.nc'):
        filename += '.nc'

    dataarray.to_netcdf(filename)
