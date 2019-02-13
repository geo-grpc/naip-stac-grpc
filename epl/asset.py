"""
Copyright 2017-2018 Echo Park Labs

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

For additional information, contact:

email: info@echoparklabs.io
"""

from epl.protobuf import stac_pb2, stac_item_result_pb2

asset_map = {
    'UNKNOWN_ASSET': 0,
    'JPEG': 1,
    'GEOTIFF': 2,
    'LERC': 3,
    'META_RASTER_FORMAT': 4,
}

naip_s3_assets = {
    stac_pb2.GEOTIFF: 'tif',
    stac_pb2.LERC: 'lrc',
    stac_pb2.MRF: 'mrf',
    stac_pb2.MRF_IDX: 'idx',
    stac_pb2.MRF_XML: 'xml'
}


def write_asset(s3_path_template: str,
                band_type: stac_pb2.EO_BAND,
                asset_type: stac_pb2.ASSET_TYPE,
                metadata_asset_map):
    extension = naip_s3_assets[asset_type]
    s3_path = s3_path_template + extension
    asset = stac_item_result_pb2.Asset(eo_band=band_type,
                                       bucket_iaas_host=stac_pb2.AWS,
                                       bucket_ref=s3_path,
                                       asset_type=asset_type)

    asset_band_key = "{0}-{1}".format(stac_pb2.ASSET_TYPE.Name(asset_type), stac_pb2.EO_BAND.Name(band_type))

    metadata_asset_map[asset_band_key].CopyFrom(asset)


def extract_naip_s3_path(metadata_request: stac_pb2.MetadataRequest,
                         state: str,
                         year: int,
                         usgsid: str,
                         image_name: str,
                         metadata_result: stac_item_result_pb2.MetadataResult):
    if metadata_request.eo_bands == stac_pb2.RGB_BANDS:
        return

    resolution = '100cm' if metadata_result.eo_gsd == 1 else "60cm"

    bucket_list = ["naip-visualization", "naip-source", "naip-analytic"]

    for bucket in bucket_list:
        imagery_bands = stac_pb2.RGBIR_BANDS
        band_string = 'rgbir'
        if bucket == 'naip-visualization':
            imagery_bands = stac_pb2.RGB_BANDS
            band_string = 'rgb'

        s3_path_template = 's3://{0}/{1}/{2}/{3}/{4}/{5}/{6}.'.format(
            bucket,
            state,
            year,
            resolution,
            band_string,
            usgsid[:5],
            image_name[:-13])

        if bucket == 'naip-analytic':
            asset_types = [stac_pb2.MRF_XML, stac_pb2.MRF, stac_pb2.MRF_IDX, stac_pb2.LERC]
            for asset_type in asset_types:
                write_asset(s3_path_template, imagery_bands, asset_type, metadata_result.assets)
        else:
            write_asset(s3_path_template, imagery_bands, stac_pb2.GEOTIFF, metadata_result.assets)
