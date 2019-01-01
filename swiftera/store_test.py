import unittest
from epl.protobuf import geometry_operators_pb2 as geometry
from epl.protobuf import stac_pb2 as stac
from swiftera import store
from swiftera import parse as store2
from google.protobuf.timestamp_pb2 import Timestamp

from datetime import datetime, timezone

from sqlalchemy import Table, Column, Integer, String, MetaData, Date, Float, create_engine
from geoalchemy2 import Geometry
from sqlalchemy.sql import select, and_

metadata = MetaData()
naip_visual = Table('naip_visual', metadata,
                    Column('ogc_fid', Integer, primary_key=True),
                    Column('filename', String),
                    Column('srcimgdate', Date),
                    Column('res', Float),
                    Column('st', String),
                    Column('wkb_geometry', Geometry('POLYGON')))


def timestamp_from_datetime(dt):
    ts = Timestamp()
    ts.FromDatetime(dt)
    return ts


class TestStore(unittest.TestCase):
    def setUp(self):
        engine = create_engine('postgresql://user:cabbage@localhost:5432/testdb', echo=True)
        self.postgres_access = store.PostgresStore(db_engine=engine)

    def test_simple_date_2(self):
        timestamp = Timestamp()
        timestamp.GetCurrentTime()
        dt = datetime(2014, 4, 4, 2, 23, 43)
        src_img_date = stac.TimestampField(value=timestamp_from_datetime(dt), rel_type=stac.FIELD_GREATER_EQUAL)
        metadata_req = stac.MetadataRequest(src_img_date=src_img_date)

        # https://stackoverflow.com/a/22771612/445372
        metadata_req.eo_gsd.CopyFrom(stac.DoubleField(value=.75, rel_type=stac.FIELD_LESS_EQUAL))

        limit = 40
        offset = 0
        current_and = None
        if metadata_req:
            current_and = and_(naip_visual.c.srcimgdate >= datetime.fromtimestamp(metadata_req.src_img_date.value.seconds, timezone.utc))
        s = select([naip_visual], current_and).limit(limit).offset(offset)

        # print(naip_stac.FieldName.Name(req.query.field_info.field_name))

        dt = datetime.fromtimestamp(metadata_req.src_img_date.value.seconds, timezone.utc)

        conn = self.postgres_access.db_engine.connect()
        result = conn.execute(s)
        for row in result:
            print(row)
        print(str(dt))
        self.assertEqual(0, 0)

    def test_simple_gsd_1(self):
        metadata_request = stac.MetadataRequest(eo_gsd=stac.DoubleField(value=0.75))
        query = self.postgres_access.construct_query(metadata_request)
        result = self.postgres_access.execute_query(query)
        self.assertEqual(0, len(list(result)))

    def test_simple_gsd_2(self):
        metadata_request = stac.MetadataRequest(eo_gsd=stac.DoubleField(value=0.6))
        query = self.postgres_access.construct_query(metadata_request)
        result = self.postgres_access.execute_query(query)
        self.assertEqual(100, len(list(result)))

    def test_simple_gsd_3(self):
        metadata_request = stac.MetadataRequest(eo_gsd=stac.DoubleField(value=0.6, rel_type=stac.FIELD_NOT_EQUAL))
        query = self.postgres_access.construct_query(metadata_request)
        result = self.postgres_access.execute_query(query)
        for row in result:
            self.assertNotEqual(row[3], 0.6)

    def test_simple_date_3(self):
        timestamp = Timestamp()
        timestamp.GetCurrentTime()

        src_img_date = stac.TimestampField(value=timestamp, rel_type=stac.FIELD_GREATER_EQUAL)
        metadata_request = stac.MetadataRequest(src_img_date=src_img_date)

        query = self.postgres_access.construct_query(metadata_request)
        result = self.postgres_access.execute_query(query)
        self.assertEqual(0, len(list(result)))

    def test_simple_date_4(self):
        engine = create_engine('postgresql://user:cabbage@localhost:5432/testdb', echo=True)
        timestamp = Timestamp()
        timestamp.GetCurrentTime()

        src_img_date = stac.TimestampField(value=timestamp, rel_type=stac.FIELD_LESS)
        metadata_request = stac.MetadataRequest(src_img_date=src_img_date)

        query = self.postgres_access.construct_query(metadata_request)
        result = self.postgres_access.execute_query(query)
        stuff = list(result)
        self.assertEqual(100, len(stuff))
        print(stuff[0])

    def test_complex_date(self):
        timestamp = timestamp_from_datetime(datetime(2012, 6, 28))
        timestamp_range = timestamp_from_datetime(datetime(2012, 6, 30))
        src_img_date = stac.TimestampField(value=timestamp, rel_type=stac.FIELD_RANGE, range_value=timestamp_range)
        metadata_request = stac.MetadataRequest(src_img_date=src_img_date)

        query = self.postgres_access.construct_query(metadata_request)
        result = self.postgres_access.execute_query(query)
        stuff = list(result)
        self.assertEqual(100, len(stuff))
        for s in stuff:
            self.assertGreaterEqual(s[2], datetime(2012, 6, 28).date())
            self.assertLess(s[2], datetime(2012, 6, 30).date())

    def test_date_range_and_double(self):
        # date range to search
        timestamp = timestamp_from_datetime(datetime(2012, 6, 28))
        timestamp_range = timestamp_from_datetime(datetime(2012, 6, 30))
        src_img_date = stac.TimestampField(value=timestamp, rel_type=stac.FIELD_RANGE, range_value=timestamp_range)

        # gsd value
        eo_gsd = stac.DoubleField(value=0.6)

        # request object
        metadata_request = stac.MetadataRequest(src_img_date=src_img_date, eo_gsd=eo_gsd)

        query = self.postgres_access.construct_query(metadata_request)
        result = self.postgres_access.execute_query(query)
        stuff = list(result)
        self.assertEqual(0, len(stuff))

    def test_complex_1(self):
        # date range to search
        timestamp = timestamp_from_datetime(datetime(2016, 8, 13))
        timestamp_range = timestamp_from_datetime(datetime(2018, 8, 13))
        src_img_date = stac.TimestampField(value=timestamp, rel_type=stac.FIELD_RANGE, range_value=timestamp_range)

        # gsd value
        eo_gsd = stac.DoubleField(value=0.6)

        # state initials
        filename = stac.StringField(value="m_4112305_nw_10_h_20160813_20161004.tif")

        # request object
        metadata_request = stac.MetadataRequest(src_img_date=src_img_date,
                                                eo_gsd=eo_gsd,
                                                filename=filename)

        query = self.postgres_access.construct_query(metadata_request)
        result = self.postgres_access.execute_query(query)
        self.assertEqual(1, len(list(result)))

    def test_geometry(self):
        # 42.6609° N, 77.0539° W
        eo_geometry = stac.GeometryField(geometry=geometry.GeometryData(wkt="POINT(-77.0539 42.6609)"))
        metadata_request = stac.MetadataRequest(eo_geometry=eo_geometry)

        query = self.postgres_access.construct_query(metadata_request)
        result = list(self.postgres_access.execute_query(query))

        self.assertLessEqual(3, len(result))

    def test_metadata_results(self):
        eo_geometry = stac.GeometryField(geometry=geometry.GeometryData(wkt="POINT(-77.0539 42.6609)"))
        metadata_request = stac.MetadataRequest(eo_geometry=eo_geometry)

        query = self.postgres_access.construct_query(metadata_request)
        query_result = self.postgres_access.execute_query(query)
        for metadata_result in self.postgres_access.query_to_metadata_result(query_result):
            self.assertEqual(1.0, metadata_result.eo_gsd)
            self.assertTrue(metadata_result.filename.startswith('m_4207724_se_18_1_'))
