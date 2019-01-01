import unittest
import epl.protobuf.stac_pb2 as stac
import swiftera.store_proto2 as store2
import epl.protobuf.geometry_operators_pb2 as geometry
from sqlalchemy import create_engine
from swiftera import store


class TestProto3Stac(unittest.TestCase):
    def setUp(self):
        engine = create_engine('postgresql://user:cabbage@localhost:5432/testdb', echo=True)
        self.postgres_access = store.PostgresStore(db_engine=engine)

    def test_posty(self):
        eo_geometry = stac.GeometryField(geometry=geometry.GeometryData(wkt="POINT(-77.0539 42.6609)"))
        metadata_request = stac.MetadataRequest(eo_geometry=eo_geometry)

        query = self.postgres_access.construct_query(metadata_request)
        query_result = self.postgres_access.execute_query(query)
        headers = [y[0] for y in query_result.context.result_column_struct[0]]
        for query_result_row in query_result:
            store2.query_to_metadata(query_result_row, headers, self.postgres_access)
