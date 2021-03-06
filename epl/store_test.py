import unittest
import os

from datetime import datetime, timezone

from sqlalchemy import Table, Column, Integer, String, MetaData, Date, Float, create_engine
from geoalchemy2 import Geometry
from sqlalchemy.sql import select, and_
from google.protobuf.timestamp_pb2 import Timestamp

from epl.protobuf import geometry_pb2
from epl.protobuf import stac_pb2 as stac
from epl import store, parse

POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', 5432)

metadata = MetaData()
naip_visual = Table('naip_visual', metadata,
                    Column('ogc_fid', Integer, primary_key=True),
                    Column('filename', String),
                    Column('srcimgdate', Date),
                    Column('res', Float),
                    Column('st', String),
                    Column('wkb_geometry', Geometry('POLYGON')))


class TestStore(unittest.TestCase):
    def setUp(self):
        engine = create_engine('postgresql://user:cabbage@{0}:{1}/testdb'.format(POSTGRES_HOST, POSTGRES_PORT),
                               echo=True)
        self.postgres_access = store.PostgresStore(db_engine=engine)

    def test_simple_date_2(self):
        timestamp = Timestamp()
        timestamp.GetCurrentTime()
        dt = datetime(2014, 4, 4, 2, 23, 43)
        src_img_date = stac.TimestampField(value=parse.timestamp_from_datetime(dt), rel_type=stac.FIELD_GREATER_EQUAL)
        metadata_req = stac.MetadataRequest(src_img_date=src_img_date)

        # https://stackoverflow.com/a/22771612/445372
        metadata_req.eo_gsd.CopyFrom(stac.FloatField(value=.75, rel_type=stac.FIELD_LESS_EQUAL))

        limit = 40
        offset = 0
        current_and = None
        if metadata_req:
            current_and = and_(naip_visual.c.srcimgdate >= datetime.fromtimestamp(
                metadata_req.src_img_date.value.seconds, timezone.utc))
        s = select([naip_visual], current_and).limit(limit).offset(offset)

        conn = self.postgres_access.db_engine.connect()
        result = conn.execute(s)
        self.assertEqual(40, len(list(result)))

    def test_simple_gsd_1(self):
        metadata_request = stac.MetadataRequest(eo_gsd=stac.FloatField(value=0.75))
        query = self.postgres_access.construct_query(metadata_request)
        result = self.postgres_access.execute_query(query)
        self.assertEqual(0, len(list(result)))

    def test_simple_gsd_2(self):
        metadata_request = stac.MetadataRequest(eo_gsd=stac.FloatField(value=0.6, rel_type=stac.FIELD_LESS_EQUAL))
        query = self.postgres_access.construct_query(metadata_request)
        result = self.postgres_access.execute_query(query)
        self.assertEqual(100, len(list(result)))

    def test_simple_gsd_3(self):
        metadata_request = stac.MetadataRequest(eo_gsd=stac.FloatField(value=0.6, rel_type=stac.FIELD_NOT_EQUAL))
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
        timestamp = Timestamp()
        timestamp.GetCurrentTime()

        src_img_date = stac.TimestampField(value=timestamp, rel_type=stac.FIELD_LESS)
        metadata_request = stac.MetadataRequest(src_img_date=src_img_date)

        query = self.postgres_access.construct_query(metadata_request)
        result = self.postgres_access.execute_query(query)
        stuff = list(result)
        self.assertEqual(100, len(stuff))

    def test_complex_date(self):
        timestamp = parse.timestamp_from_datetime(datetime(2012, 6, 28))
        timestamp_range = parse.timestamp_from_datetime(datetime(2012, 6, 30))
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
        timestamp = parse.timestamp_from_datetime(datetime(2012, 6, 28))
        timestamp_range = parse.timestamp_from_datetime(datetime(2012, 6, 30))
        src_img_date = stac.TimestampField(value=timestamp, rel_type=stac.FIELD_RANGE, range_value=timestamp_range)

        # gsd value
        eo_gsd = stac.FloatField(value=0.6)

        # request object
        metadata_request = stac.MetadataRequest(src_img_date=src_img_date, eo_gsd=eo_gsd)

        query = self.postgres_access.construct_query(metadata_request)
        result = self.postgres_access.execute_query(query)
        stuff = list(result)
        self.assertEqual(0, len(stuff))

    def test_complex_1(self):
        # date range to search
        timestamp = parse.timestamp_from_datetime(datetime(2016, 8, 13))
        timestamp_range = parse.timestamp_from_datetime(datetime(2016, 8, 13))
        src_img_date = stac.TimestampField(value=timestamp, rel_type=stac.FIELD_RANGE, range_value=timestamp_range)

        # gsd value
        eo_gsd = stac.FloatField(value=0.6, rel_type=stac.FIELD_LESS_EQUAL)

        # the file name isn't the id, we're just placing it here for now
        id = stac.StringField(value="m_4112305_nw_10_h_20160813_20161004.tif")

        # request object
        metadata_request = stac.MetadataRequest(src_img_date=src_img_date,
                                                eo_gsd=eo_gsd,
                                                id=id)

        query = self.postgres_access.construct_query(metadata_request)
        result = self.postgres_access.execute_query(query)
        self.assertEqual(1, len(list(result)))

    def test_geometry(self):
        # 42.6609° N, 77.0539° W
        eo_geometry = stac.GeometryField(geometry=geometry_pb2.GeometryData(wkt="POINT(-77.0539 42.6609)"))
        metadata_request = stac.MetadataRequest(geometry=eo_geometry)

        query = self.postgres_access.construct_query(metadata_request)
        result = list(self.postgres_access.execute_query(query))

        self.assertLessEqual(3, len(result))

    def test_envelope(self):
        eo_envelope = geometry_pb2.EnvelopeData(xmin=-77.06831821412604,
                                                ymin=42.62239034158332,
                                                xmax=-76.99425409850738,
                                                ymax=42.69010108687761,
                                                spatial_reference=geometry_pb2.SpatialReferenceData(wkid=4326))
        metadata_request = stac.MetadataRequest(bbox=eo_envelope)
        query = self.postgres_access.construct_query(metadata_request)
        result = list(self.postgres_access.execute_query(query))

        self.assertLessEqual(3, len(result))

    def test_metadata_results(self):
        eo_geometry = stac.GeometryField(geometry=geometry_pb2.GeometryData(wkt="POINT(-77.0539 42.6609)"))
        metadata_request = stac.MetadataRequest(geometry=eo_geometry)

        query = self.postgres_access.construct_query(metadata_request)
        query_result = self.postgres_access.execute_query(query)
        for metadata_result in self.postgres_access.query_to_metadata_result(query_result, metadata_request):
            self.assertEqual(1.0, metadata_result.eo_gsd)
            self.assertTrue(metadata_result.HasField("eo_gsd"))

            self.assertFalse(metadata_result.HasField("eo_sun_elevation"))
            self.assertEqual(0.0, metadata_result.eo_sun_elevation)

            self.assertTrue(metadata_result.HasField("geometry"))

            for key in metadata_result.assets:
                asset = metadata_result.assets[key]
                self.assertTrue(asset.bucket_ref.startswith("s3://naip-"))
                self.assertEqual(stac.AWS, asset.bucket_iaas_host)
                asset_band_key = "{0}-{1}".format(stac.ASSET_TYPE.Name(asset.asset_type),
                                                  stac.EO_BAND.Name(asset.eo_band))
                self.assertEqual(key, asset_band_key)
                self.assertLess(0, asset.eo_band & stac.GREEN_BAND)
                self.assertLess(0, asset.eo_band & stac.BLUE_BAND)
                self.assertLess(0, asset.eo_band & stac.RED_BAND)
                self.assertLess(0, asset.eo_band & stac.RGB_BANDS)

                self.assertEqual(0, asset.eo_band & stac.SWIR_16_BAND)
