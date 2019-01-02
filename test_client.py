import logging
import os
import re
import grpc

import epl.protobuf.stac_pb2 as stac
import epl.grpc.naip_stac_pb2_grpc as naip_grpc
import epl.protobuf.geometry_operators_pb2 as geometry


logger = logging.getLogger(__name__)

MB = 1024 * 1024
GRPC_CHANNEL_OPTIONS = [('grpc.max_message_length', 64 * MB), ('grpc.max_receive_message_length', 64 * MB)]
GRPC_SERVICE_PORT = os.getenv('GRPC_SERVICE_PORT', 50051)
GRPC_SERVICE_HOST = os.getenv('GRPC_SERVICE_HOST', 'localhost')
IMAGERY_SERVICE = "{0}:{1}".format(GRPC_SERVICE_HOST, GRPC_SERVICE_PORT)
ip_reg = re.compile(r"[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}")

if GRPC_SERVICE_HOST == "localhost" or ip_reg.match(GRPC_SERVICE_HOST):
    channel = grpc.insecure_channel(IMAGERY_SERVICE, options=GRPC_CHANNEL_OPTIONS)
else:
    channel_credentials = grpc.ssl_channel_credentials()
    channel = grpc.secure_channel(IMAGERY_SERVICE, credentials=channel_credentials, options=GRPC_CHANNEL_OPTIONS)

stub = naip_grpc.MetadataOperatorsStub(channel)


if __name__ == '__main__':
    print('pancakes')
    eo_geometry = stac.GeometryField(geometry=geometry.GeometryData(wkt="POINT(-77.0539 42.6609)"))
    metadata_request = stac.MetadataRequest(geometry=eo_geometry,
                                            eo_gsd=stac.FloatField(value=1.0, rel_type=stac.FIELD_LESS_EQUAL))

    results_generator = stub.Search(metadata_request)
    for metadata_result in results_generator:
        assets = metadata_result.assets
        for asset_key in assets:
            asset = assets[asset_key]
            print(asset.bucket_ref)
            print(stac.IAAS.Name(asset.bucket_iaas_host))
