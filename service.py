"""
/*
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
*/
"""

import grpc
import time
import os
from epl.protobuf import stac_pb2
import epl.grpc.naip_stac_pb2_grpc as naip_grpc
import epl.store as store

from concurrent import futures
from sqlalchemy import create_engine

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

GRPC_PORT = os.getenv('GRPC_PORT', 50051)

GRPC_CHAIN = os.getenv('GRPC_CHAIN', None)
GRPC_KEY = os.getenv('GRPC_KEY', None)

MAX_MESSAGE_MB = os.getenv('MAX_MESSAGE_MB', 64)
BYTES_PER_MB = 1024 * 1024
# https://github.com/grpc/grpc/issues/7927
GRPC_CHANNEL_OPTIONS = [
    ('grpc.max_message_length', MAX_MESSAGE_MB * BYTES_PER_MB),
    ('grpc.max_receive_message_length', MAX_MESSAGE_MB * BYTES_PER_MB)]


class MetadataServicer(naip_grpc.MetadataOperatorsServicer):
    def __init__(self, db_engine):
        self.db_engine = db_engine
        self.postgres_access = store.PostgresStore(db_engine=db_engine)
        print("started metadata service")

    def Search(self,
               metadata_request: stac_pb2.MetadataRequest,
               context) -> stac_pb2.MetadataResult:
        query = self.postgres_access.construct_query(metadata_request)
        query_result = self.postgres_access.execute_query(query)
        for metadata_result in self.postgres_access.query_to_metadata_result(query_result, metadata_request):
            yield metadata_result


def serve():
    # grpc server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=GRPC_CHANNEL_OPTIONS)

    # db connection
    engine = create_engine('postgresql://user:cabbage@localhost:5432/testdb', echo=True)

    # add metadata service
    naip_grpc.add_MetadataOperatorsServicer_to_server(MetadataServicer(engine), server)

    # define port to run on
    port_address = '[::]:{0}'.format(os.getenv('GRPC_SERVICE_PORT', 50051))

    # create server credentials
    if GRPC_CHAIN is None or GRPC_KEY is None or not os.path.isfile(GRPC_KEY) or not os.path.isfile(GRPC_CHAIN):
        print("adding insecure port")
        server.add_insecure_port(address=port_address)
    else:
        # read in key and certificate
        with open(GRPC_KEY, 'rb') as f:
            private_key = f.read()
        with open(GRPC_CHAIN, 'rb') as f:
            certificate_chain = f.read()
        server_credentials = grpc.ssl_server_credentials(((private_key, certificate_chain,),))
        print("adding secure port")
        server.add_secure_port(address=port_address, server_credentials=server_credentials)

    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
