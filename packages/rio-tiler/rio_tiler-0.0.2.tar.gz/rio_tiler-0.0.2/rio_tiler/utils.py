"""rio_tiler.utils: utility functions."""

import os
import re
import base64
import datetime
from io import BytesIO

import numpy as np

import mercantile

import rasterio
from rasterio.vrt import WarpedVRT
from rasterio.enums import Resampling
from rio_toa import reflectance, toa_utils

from rio_tiler.errors import (InvalidFormat,
                              InvalidLandsatSceneId,
                              InvalidSentinelSceneId)

from PIL import Image

# Python 2/3
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen


def landsat_min_max_worker(band, address, metadata, pmin=2, pmax=98,
                           width=1024, height=1024):
    """Retrieve histogram percentage cut for a Landsat-8 scene.

    Attributes
    ----------

    address : Landsat band AWS address
    band : Landsat band number
    metadata : Landsat metadata
    pmin : Histogram minimum cut (default: 2)
    pmax : Histogram maximum cut (default: 98)
    width : int, optional (default: 1024)
        Pixel width for the decimated read.
    height : int, optional (default: 1024)
        Pixel height for the decimated read.

    Returns
    -------
    out : list, int
        returns a list of the min/max histogram cut values.
    """

    multi_reflect = metadata['RADIOMETRIC_RESCALING'].get(
        'REFLECTANCE_MULT_BAND_{}'.format(band))
    add_reflect = metadata['RADIOMETRIC_RESCALING'].get(
        'REFLECTANCE_ADD_BAND_{}'.format(band))
    sun_elev = metadata['IMAGE_ATTRIBUTES']['SUN_ELEVATION']

    with rasterio.open('{}_B{}.TIF'.format(address, band)) as src:
        arr = src.read(indexes=1,
                       out_shape=(height, width)).astype(src.profile['dtype'])
        arr = 10000 * reflectance.reflectance(arr, multi_reflect, add_reflect,
                                              sun_elev, src_nodata=0)

    return np.percentile(arr[arr > 0], (pmin, pmax)).astype(np.int).tolist()


def sentinel_min_max_worker(address, pmin=2, pmax=98, width=1024, height=1024):
    """Retrieve histogram percentage cut for a Sentinel-2 scene.

    Attributes
    ----------

    address : Sentinel-2 band AWS address
    pmin : Histogram minimum cut (default: 2)
    pmax : Histogram maximum cut (default: 98)
    width : int, optional (default: 1024)
        Pixel width for the decimated read.
    height : int, optional (default: 1024)
        Pixel height for the decimated read.

    Returns
    -------
    out : list, int
        returns a list of the min/max histogram cut values.
    """

    with rasterio.open(address) as src:
        arr = src.read(indexes=1,
                       out_shape=(height, width)).astype(src.profile['dtype'])

    return np.percentile(arr[arr > 0], (pmin, pmax)).astype(np.int).tolist()


def tile_band_worker(address, bounds, tilesize, indexes=[1], nodata=0):
    """Read band data

    Attributes
    ----------

    address : Sentinel-2/Landsat-8 band AWS address
    bounds : Mercator tile bounds to retrieve
    tilesize : Output image size
    indexes : list of ints or a single int, optional, (default: 1)
        If `indexes` is a list, the result is a 3D array, but is
        a 2D array if it is a band index number.
    nodata: int or float, optional (defaults: 0)

    Returns
    -------
    out : array, int
        returns pixel value.
    """
    w, s, e, n = bounds

    out_shape = (tilesize, tilesize)

    if not isinstance(indexes, int):
        if len(indexes) == 1:
            indexes = indexes[0]
        else:
            out_shape = (len(indexes),) + out_shape

    with rasterio.open(address) as src:
        with WarpedVRT(src,
                       dst_crs='EPSG:3857',
                       resampling=Resampling.bilinear,
                       src_nodata=nodata,
                       dst_nodata=nodata) as vrt:
                            window = vrt.window(w, s, e, n, precision=21)
                            return vrt.read(window=window,
                                            boundless=True,
                                            resampling=Resampling.bilinear,
                                            out_shape=out_shape,
                                            indexes=indexes)


def linear_rescale(image, in_range=(0, 1), out_range=(1, 255)):
    """Linear rescaling

    Attributes
    ----------

    image : numpy ndarray
        Image array to rescale.
    in_range : list, int, optional, (default: [0,1])
        Image min/max value to rescale.
    out_range : list, int, optional, (default: [1,255])
        output min/max bounds to rescale to.

    Returns
    -------
    out : numpy ndarray
        returns rescaled image array.
    """

    imin, imax = in_range
    omin, omax = out_range
    image = np.clip(image, imin, imax) - imin
    image = image / np.float(imax - imin)
    return image * (omax - omin) + omin


def tile_exists(bounds, tile_z, tile_x, tile_y):
    """Check if a mercatile tile is inside a given bounds

    Attributes
    ----------

    bounds : list
        WGS84 bounds (left, bottom, right, top).
    x : int
        Mercator tile Y index.
    y : int
        Mercator tile Y index.
    z : int
        Mercator tile ZOOM level.

    Returns
    -------
    out : boolean
        if True, the z-x-y mercator tile in inside the bounds.
    """

    mintile = mercantile.tile(bounds[0], bounds[3], tile_z)
    maxtile = mercantile.tile(bounds[2], bounds[1], tile_z)

    return (tile_x <= maxtile.x + 1) \
        and (tile_x >= mintile.x) \
        and (tile_y <= maxtile.y + 1) \
        and (tile_y >= mintile.y)


def landsat_get_mtl(sceneid):
    """Get Landsat-8 MTL metadata

    Attributes
    ----------

    sceneid : str
        Landsat sceneid. For scenes after May 2017,
        sceneid have to be LANDSAT_PRODUCT_ID.

    Returns
    -------
    out : dict
        returns a JSON like object with the metadata.
    """

    try:
        scene_params = landsat_parse_scene_id(sceneid)
        meta_file = 'http://landsat-pds.s3.amazonaws.com/{}_MTL.txt'.format(scene_params['key'])
        metadata = str(urlopen(meta_file).read().decode())
        return toa_utils._parse_mtl_txt(metadata)
    except:
        raise Exception('Could not retrieve {} metadata'.format(sceneid))


def landsat_parse_scene_id(sceneid):
    """Parse Landsat-8 scene id

    Author @perrygeo - http://www.perrygeo.com
    """

    pre_collection = r'(L[COTEM]8\d{6}\d{7}[A-Z]{3}\d{2})'
    collection_1 = r'(L[COTEM]08_L\d{1}[A-Z]{2}_\d{6}_\d{8}_\d{8}_\d{2}_(T1|T2|RT))'
    if not re.match('^{}|{}$'.format(pre_collection, collection_1), sceneid):
        raise InvalidLandsatSceneId('Could not match {}'.format(sceneid))

    precollection_pattern = (
        r'^L'
        r'(?P<sensor>\w{1})'
        r'(?P<satellite>\w{1})'
        r'(?P<path>[0-9]{3})'
        r'(?P<row>[0-9]{3})'
        r'(?P<acquisitionYear>[0-9]{4})'
        r'(?P<acquisitionJulianDay>[0-9]{3})'
        r'(?P<groundStationIdentifier>\w{3})'
        r'(?P<archiveVersion>[0-9]{2})$')

    collection_pattern = (
        r'^L'
        r'(?P<sensor>\w{1})'
        r'(?P<satellite>\w{2})'
        r'_'
        r'(?P<processingCorrectionLevel>\w{4})'
        r'_'
        r'(?P<path>[0-9]{3})'
        r'(?P<row>[0-9]{3})'
        r'_'
        r'(?P<acquisitionYear>[0-9]{4})'
        r'(?P<acquisitionMonth>[0-9]{2})'
        r'(?P<acquisitionDay>[0-9]{2})'
        r'_'
        r'(?P<processingYear>[0-9]{4})'
        r'(?P<processingMonth>[0-9]{2})'
        r'(?P<processingDay>[0-9]{2})'
        r'_'
        r'(?P<collectionNumber>\w{2})'
        r'_'
        r'(?P<collectionCategory>\w{2})$')

    meta = None
    for pattern in [collection_pattern, precollection_pattern]:
        match = re.match(pattern, sceneid, re.IGNORECASE)
        if match:
            meta = match.groupdict()
            break

    if meta.get('acquisitionJulianDay'):
        date = datetime.datetime(int(meta['acquisitionYear']), 1, 1) \
            + datetime.timedelta(int(meta['acquisitionJulianDay']) - 1)

        meta['date'] = date.strftime('%Y-%m-%d')
    else:
        meta['date'] = '{}-{}-{}'.format(
            meta['acquisitionYear'], meta['acquisitionMonth'],
            meta['acquisitionDay'])

    collection = meta.get('collectionNumber', '')
    if collection != '':
        collection = 'c{}'.format(int(collection))

    meta['key'] = os.path.join(collection, 'L8', meta['path'], meta['row'],
                               sceneid, sceneid)

    meta['scene'] = sceneid

    return meta


def sentinel_parse_scene_id(sceneid):
    """Parse Sentinel-2 scene id"""

    if not re.match('^S2[AB]_tile_[0-9]{8}_[0-9]{2}[A-Z]{3}_[0-9]$', sceneid):
        raise InvalidSentinelSceneId('Could not match {}'.format(sceneid))

    sentinel_pattern = (
        r'^S'
        r'(?P<sensor>\w{1})'
        r'(?P<satellite>[AB]{1})'
        r'_tile_'
        r'(?P<acquisitionYear>[0-9]{4})'
        r'(?P<acquisitionMonth>[0-9]{2})'
        r'(?P<acquisitionDay>[0-9]{2})'
        r'_'
        r'(?P<utm>[0-9]{2})'
        r'(?P<sq>\w{1})'
        r'(?P<lat>\w{2})'
        r'_'
        r'(?P<num>[0-9]{1})$')

    meta = None
    match = re.match(sentinel_pattern, sceneid, re.IGNORECASE)
    if match:
        meta = match.groupdict()

    utm_zone = meta['utm']
    grid_square = meta['sq']
    latitude_band = meta['lat']
    year = meta['acquisitionYear']
    month = meta['acquisitionMonth'].lstrip("0")
    day = meta['acquisitionDay'].lstrip("0")
    img_num = meta['num']

    meta['key'] = 'tiles/{}/{}/{}/{}/{}/{}/{}'.format(
        utm_zone, grid_square, latitude_band, year, month, day, img_num)

    return meta


def array_to_img(arr, tileformat='png', nodata=0):
    """Convert an array to an base64 encoded img

    Attributes
    ----------

    arr : numpy ndarray
        Image array to encode.
    tileformat : str (default: png)
        Image format to return (Accepted: "jpg" or "png")

    Returns
    -------
    out : str
        base64 encoded PNG or JPEG image.
    """

    if tileformat not in ['png', 'jpg']:
        raise InvalidFormat('Invalid {} extension'.format(tileformat))

    # https://pillow.readthedocs.io/en/4.3.x/handbook/concepts.html#concept-modes
    if arr.ndim == 2:
        img = Image.fromarray(arr, mode='L')
    else:
        mask_shape = (1,) + arr.shape[-2:]
        mask = np.full(mask_shape, 255, dtype=np.uint8)
        if nodata is not None:
            mask[0] = np.all(np.dstack(arr) != nodata, axis=2).astype(np.uint8) * 255
        arr = np.concatenate((arr, mask))
        img = Image.fromarray(np.stack(arr, axis=2))

    sio = BytesIO()
    if tileformat == 'jpg':
        img = img.convert('RGB')
        img.save(sio, 'jpeg', subsampling=0, quality=100)
    else:
        img.save(sio, 'png', compress_level=0)

    sio.seek(0)

    return base64.b64encode(sio.getvalue()).decode()
