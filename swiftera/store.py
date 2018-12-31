from epl.protobuf import stac_pb2 as stac

from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime, timezone

from sqlalchemy import Table, Column, Integer, String, MetaData, Date, Float, create_engine
from geoalchemy2 import Geometry
from geoalchemy2.elements import WKTElement
from sqlalchemy.sql import select, and_

metadata = MetaData()
naip_visual = Table('naip_visual', metadata,
                    Column('ogc_fid', Integer, primary_key=True),
                    Column('filename', String),
                    Column('srcimgdate', Date),
                    Column('res', Float),
                    Column('st', String),
                    Column('wkb_geometry', Geometry('POLYGON')))

message_db_map = {
    # it's longer to type this all out, but it ensures at compile time that these values exist in proto definition
    stac.MetadataRequest2.DESCRIPTOR.fields_by_name['eo_gsd'].name: 'res',
    stac.MetadataRequest2.DESCRIPTOR.fields_by_name['src_img_date'].name: 'srcimgdate',
    stac.MetadataRequest2.DESCRIPTOR.fields_by_name['filename'].name: 'filename',
    stac.MetadataRequest2.DESCRIPTOR.fields_by_name['state_initials'].name: 'st',
stac.MetadataRequest2.DESCRIPTOR.fields_by_name['eo_geometry'].name: 'wkb_geometry',
}


def add_and(query_filter, current_and=None):
    if current_and is None:
        return query_filter
    return and_(query_filter, current_and)


def timestamp_from_datetime(dt):
    ts = Timestamp()
    ts.FromDatetime(dt)
    return ts


def construct_query(message: stac):

    current_and = None
    # parsing https://stackoverflow.com/a/29150312/445372
    for field in message.DESCRIPTOR.fields:
        if field.type != field.TYPE_MESSAGE:
            continue
        if message.HasField(field.name):
            full_name = field.message_type.full_name
            field_obj = getattr(message, field.name)
            mapped_field = message_db_map[field.name]
            value1 = getattr(field_obj, "value")

            if full_name == stac.BBoxField.DESCRIPTOR.full_name:
                print(full_name)
            elif full_name == stac.GeometryField.DESCRIPTOR.full_name:
                wkt = WKTElement(value1.wkt[0], srid=4326)
                current_and = add_and(naip_visual.c.wkb_geometry.ST_Intersects(wkt), current_and)
            elif full_name == stac.DoubleField.DESCRIPTOR.full_name or \
                    full_name == stac.Int64Field.DESCRIPTOR.full_name or \
                    full_name == stac.TimestampField.DESCRIPTOR.full_name or \
                    full_name == stac.StringField.DESCRIPTOR.full_name:

                rel_type = getattr(field_obj, "rel_type")
                value2 = getattr(field_obj, "range_value")
                if full_name == stac.TimestampField.DESCRIPTOR.full_name:
                    value1 = datetime.fromtimestamp(getattr(value1, "seconds"), timezone.utc)
                    value2 = datetime.fromtimestamp(getattr(value2, "seconds"), timezone.utc)

                if rel_type == stac.FIELD_EQUALS:
                    current_and = add_and(naip_visual.c[mapped_field] == value1, current_and)
                elif rel_type == stac.FIELD_NOT_EQUAL:
                    current_and = add_and(naip_visual.c[mapped_field] != value1, current_and)
                elif rel_type == stac.FIELD_GREATER_EQUAL:
                    current_and = add_and(naip_visual.c[mapped_field] >= value1, current_and)
                elif rel_type == stac.FIELD_LESS_EQUAL:
                    current_and = add_and(naip_visual.c[mapped_field] <= value1, current_and)
                elif rel_type == stac.FIELD_RANGE:
                    current_and = add_and(naip_visual.c[mapped_field] >= value1, current_and)
                    current_and = add_and(naip_visual.c[mapped_field] <= value2, current_and)
                elif rel_type == stac.FIELD_NOT_RANGE:
                    current_and = add_and(naip_visual.c[mapped_field] < value1, current_and)
                    current_and = add_and(naip_visual.c[mapped_field] > value2, current_and)

    return current_and


def execute_query(query_filter, engine, limit=100, offset=0):
    s = select([naip_visual], query_filter).limit(limit)
    conn = engine.connect()
    result = conn.execute(s)
    return result
