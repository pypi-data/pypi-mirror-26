"""rio_tiler.landsat8: Landsat-8 processing."""

from functools import partial
from concurrent import futures

import numpy as np
from cachetools.func import lru_cache

import mercantile
from rasterio import Affine
from rasterio import transform

from rio_toa import reflectance, toa_utils
from rio_pansharpen.worker import pansharpen

from rio_tiler import utils
from rio_tiler.errors import TileOutsideBounds


LANDSAT_BUCKET = 's3://landsat-pds'


@lru_cache()
def bounds(sceneid):
    """Retrieve image bounds.

    Attributes
    ----------

    sceneid : str
        Landsat sceneid. For scenes after May 2017,
        sceneid have to be LANDSAT_PRODUCT_ID.

    Returns
    -------
    out : dict
        dictionary with image bounds.
    """

    meta_data = utils.landsat_get_mtl(sceneid).get('L1_METADATA_FILE')

    info = {'sceneid': sceneid}
    info['bounds'] = toa_utils._get_bounds_from_metadata(
        meta_data['PRODUCT_METADATA'])

    return info


@lru_cache()
def metadata(sceneid, pmin=2, pmax=98):
    """Retrieve image bounds and histogram info.

    Attributes
    ----------

    sceneid : str
        Landsat sceneid. For scenes after May 2017,
        sceneid have to be LANDSAT_PRODUCT_ID.
    pmin : int, optional, (default: 2)
        Histogram minimum cut.
    pmax : int, optional, (default: 98)
        Histogram maximum cut.

    Returns
    -------
    out : dict
        dictionary with image bounds and bands histogram cuts.
    """

    scene_params = utils.landsat_parse_scene_id(sceneid)
    meta_data = utils.landsat_get_mtl(sceneid).get('L1_METADATA_FILE')
    landsat_address = '{}/{}'.format(LANDSAT_BUCKET, scene_params['key'])

    info = {'sceneid': sceneid}
    info['bounds'] = toa_utils._get_bounds_from_metadata(
        meta_data['PRODUCT_METADATA'])

    bands = ['1', '2', '3', '4', '5', '6', '7']
    _min_max_worker = partial(utils.landsat_min_max_worker,
                              address=landsat_address,
                              metadata=meta_data,
                              pmin=pmin,
                              pmax=pmax)

    with futures.ThreadPoolExecutor(max_workers=7) as executor:
        responses = list(executor.map(_min_max_worker, bands))
        info['rgbMinMax'] = dict(zip(bands, responses))

    return info


@lru_cache()
def tile(sceneid, tile_x, tile_y, tile_z, rgb=(4, 3, 2), r_bds=(0, 16000),
         g_bds=(0, 16000), b_bds=(0, 16000), tilesize=256, pan=False):
    """Create mercator tile from Landsat-8 data and encodes it in base64.

    Attributes
    ----------

    sceneid : str
        Landsat sceneid. For scenes after May 2017,
        sceneid have to be LANDSAT_PRODUCT_ID.
    tile_x : int
        Mercator tile X index.
    tile_y : int
        Mercator tile Y index.
    tile_z : int
        Mercator tile ZOOM level.
    rgb : tuple, int, optional (default: (4, 3, 2))
        Bands index for the RGB combination.
    r_bds : tuple, int, optional (default: (0, 16000))
        First band (red) DN min and max values (DN * 10,000)
        used for the linear rescaling.
    g_bds : tuple, int, optional (default: (0, 16000))
        Second band (green) DN min and max values (DN * 10,000)
        used for the linear rescaling.
    b_bds : tuple, int, optional (default: (0, 16000))
        Third band (blue) DN min and max values (DN * 10,000)
        used for the linear rescaling.
    tilesize : int, optional (default: 256)
        Output image size.
    pan : boolean, optional (default: False)
        If True, apply pan-sharpening.

    Returns
    -------
    out : numpy ndarray (type: uint8)
    """

    scene_params = utils.landsat_parse_scene_id(sceneid)
    meta_data = utils.landsat_get_mtl(sceneid).get('L1_METADATA_FILE')
    landsat_address = '{}/{}'.format(LANDSAT_BUCKET, scene_params['key'])

    wgs_bounds = toa_utils._get_bounds_from_metadata(
        meta_data['PRODUCT_METADATA'])

    if not utils.tile_exists(wgs_bounds, tile_z, tile_x, tile_y):
        raise TileOutsideBounds(
            'Tile {}/{}/{} is outside image bounds'.format(
                tile_z, tile_x, tile_y))

    mercator_tile = mercantile.Tile(x=tile_x, y=tile_y, z=tile_z)
    tile_bounds = mercantile.xy_bounds(mercator_tile)

    # define a list of bands Min and Max Values (from input)
    histo_cuts = dict(zip(rgb, [r_bds, g_bds, b_bds]))

    ms_tile_size = int(tilesize / 2) if pan else tilesize

    addresses = ['{}_B{}.TIF'.format(landsat_address, band) for band in rgb]
    _tiler = partial(utils.tile_band_worker,
                     bounds=tile_bounds,
                     tilesize=ms_tile_size)

    with futures.ThreadPoolExecutor(max_workers=3) as executor:
        out = np.stack(list(executor.map(_tiler, addresses)))

        if pan:
            pan_address = '{}_B8.TIF'.format(landsat_address)
            matrix_pan = utils.tile_band_worker(pan_address, tile_bounds, tilesize)

            w, s, e, n = tile_bounds
            pan_transform = transform.from_bounds(w, s, e, n, tilesize, tilesize)
            vis_transform = pan_transform * Affine.scale(2.)
            out = pansharpen(out, vis_transform, matrix_pan, pan_transform,
                             np.int16, 'EPSG:3857', 'EPSG:3857', 0.2,
                             method='Brovey', src_nodata=0)

        sun_elev = meta_data['IMAGE_ATTRIBUTES']['SUN_ELEVATION']

        for bdx, band in enumerate(rgb):
            multi_reflect = meta_data['RADIOMETRIC_RESCALING'].get(
                'REFLECTANCE_MULT_BAND_{}'.format(band))

            add_reflect = meta_data['RADIOMETRIC_RESCALING'].get(
                'REFLECTANCE_ADD_BAND_{}'.format(band))

            out[bdx] = 10000 * reflectance.reflectance(
                out[bdx], multi_reflect, add_reflect, sun_elev, src_nodata=0)

            out[bdx] = np.where(
                out[bdx] > 0,
                utils.linear_rescale(
                    out[bdx],
                    in_range=histo_cuts.get(band),
                    out_range=[1, 255]), 0)

    return out.astype(np.uint8)
