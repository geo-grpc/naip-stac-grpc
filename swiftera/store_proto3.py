from epl.protobuf import stac_proto3_pb2
from epl.protobuf import stac_pb2 as stac
from swiftera.store import PostgresStore
from typing import Tuple, List


def query_to_metadata(query_result_row: Tuple, headers: List, postgres_connection):
    result = stac_proto3_pb2.MetadataResult()
    for index, item in enumerate(query_result_row):
        db_key = headers[index]
        if db_key in postgres_connection.db_message_map:
            message_key = postgres_connection.db_message_map[db_key]
            setattr(result, message_key, item)

    return result
