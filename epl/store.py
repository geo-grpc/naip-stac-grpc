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

from epl.protobuf import stac_pb2 as stac
from epl.protobuf import geometry_pb2
from epl import parse, asset
from datetime import datetime, timezone

from sqlalchemy import Table, Column, Integer, String, MetaData, Date, Float
from geoalchemy2 import Geometry
from geoalchemy2.elements import WKTElement, WKBElement
from sqlalchemy.sql import select, and_
from sqlalchemy.engine.result import ResultProxy

metadata = MetaData()
naip_visual = Table('naip_visual', metadata,
                    Column('ogc_fid', Integer, primary_key=True),
                    Column('filename', String),
                    Column('srcimgdate', Date),
                    Column('res', Float),
                    Column('st', String),
                    Column('usgsid', String),
                    Column('wkb_geometry', Geometry('POLYGON')))


class PostgresStore:
    def __init__(self, db_engine):
        self.message_db_map = {
            # it's longer to type this all out, but it ensures
            # at compile time that these values exist in proto definition
            stac.MetadataRequest.DESCRIPTOR.fields_by_name['eo_gsd'].name: 'res',
            stac.MetadataRequest.DESCRIPTOR.fields_by_name['src_img_date'].name: 'srcimgdate',
            stac.MetadataRequest.DESCRIPTOR.fields_by_name['id'].name: 'filename',
            stac.MetadataRequest.DESCRIPTOR.fields_by_name['geometry'].name: 'wkb_geometry',
            stac.MetadataRequest.DESCRIPTOR.fields_by_name['usgsid'].name: 'usgsid',
            stac.MetadataRequest.DESCRIPTOR.fields_by_name['bbox'].name: 'bbox',
        }
        self.db_message_map = {}
        for key in self.message_db_map:
            self.db_message_map[self.message_db_map[key]] = key
        self.db_engine = db_engine

    @staticmethod
    def add_and(query_filter, current_and=None):
        if current_and is None:
            return query_filter
        return and_(query_filter, current_and)

    def construct_query(self, message: stac.MetadataRequest):
        current_and = None
        ignored_fields = []
        # parsing https://stackoverflow.com/a/29150312/445372
        for field in message.DESCRIPTOR.fields:
            if field.type != field.TYPE_MESSAGE:
                ignored_fields.append(field.name)
                continue
            if message.HasField(field.name):
                full_name = field.message_type.full_name
                field_obj = getattr(message, field.name)

                if full_name == geometry_pb2.EnvelopeData.DESCRIPTOR.full_name:
                    envelope_data = field_obj
                    # ooooh, this is messy :(
                    wkt_polygon = "POLYGON (({0} {1}, {2} {1}, {2} {3}, {0} {3}, {0} {1}))".format(envelope_data.xmin,
                                                                                                   envelope_data.ymin,
                                                                                                   envelope_data.xmax,
                                                                                                   envelope_data.ymax)
                    geometry_element = WKTElement(wkt_polygon, srid=4326)
                    current_and = self.add_and(naip_visual.c.wkb_geometry.ST_Intersects(geometry_element), current_and)

                elif full_name == stac.GeometryField.DESCRIPTOR.full_name:
                    if field_obj.HasField("geometry"):
                        geometry_value = getattr(field_obj, "geometry")
                        geometry_element = None
                        if geometry_value.wkt:
                            geometry_element = WKTElement(geometry_value.wkt, srid=4326)
                        elif geometry_value.wkb:
                            geometry_element = WKBElement(geometry_value.wkb, srid=4326)

                        if geometry_element is not None:
                            current_and = self.add_and(naip_visual.c.wkb_geometry.ST_Intersects(geometry_element),
                                                       current_and)
                        else:
                            # TODO log warning/error
                            print("missing geometry data")
                else:
                    mapped_field = self.message_db_map[field.name]
                    value1 = getattr(field_obj, "value")
                    rel_type = getattr(field_obj, "rel_type")
                    value2 = getattr(field_obj, "range_value")
                    if full_name == stac.TimestampField.DESCRIPTOR.full_name:
                        value1 = datetime.fromtimestamp(getattr(value1, "seconds"), timezone.utc)
                        value2 = datetime.fromtimestamp(getattr(value2, "seconds"), timezone.utc)

                    if rel_type == stac.FIELD_NOT_EQUAL:
                        current_and = self.add_and(naip_visual.c[mapped_field] != value1, current_and)
                    elif rel_type == stac.FIELD_GREATER_EQUAL:
                        current_and = self.add_and(naip_visual.c[mapped_field] >= value1, current_and)
                    elif rel_type == stac.FIELD_LESS_EQUAL:
                        current_and = self.add_and(naip_visual.c[mapped_field] <= value1, current_and)
                    elif rel_type == stac.FIELD_GREATER:
                        current_and = self.add_and(naip_visual.c[mapped_field] > value1, current_and)
                    elif rel_type == stac.FIELD_LESS:
                        current_and = self.add_and(naip_visual.c[mapped_field] < value1, current_and)
                    elif rel_type == stac.FIELD_RANGE:
                        current_and = self.add_and(naip_visual.c[mapped_field] >= value1, current_and)
                        current_and = self.add_and(naip_visual.c[mapped_field] <= value2, current_and)
                    elif rel_type == stac.FIELD_NOT_RANGE:
                        current_and = self.add_and(naip_visual.c[mapped_field] < value1, current_and)
                        current_and = self.add_and(naip_visual.c[mapped_field] > value2, current_and)
                    else:
                        current_and = self.add_and(naip_visual.c[mapped_field] == value1, current_and)

        print("IGNORING ELEMENTS {0} in SQL Query".format(', '.join(ignored_fields)))
        return current_and

    def execute_query(self, query_filter, limit=100, offset=0):
        s = select([naip_visual], query_filter).limit(limit)
        conn = self.db_engine.connect()
        query_result = conn.execute(s)
        return query_result

    def query_to_metadata_result(self, query_result: ResultProxy, metadata_request: stac.MetadataRequest) -> \
            stac.MetadataResult:
        headers = [y[0] for y in query_result.context.result_column_struct[0]]
        for query_result_row in query_result:
            metadata_result = parse.to_metadata_result(query_result_row, headers, self.db_message_map)
            asset.extract_naip_s3_path(
                metadata_request=metadata_request,
                state=query_result_row[4].lower(),
                year=query_result_row[2].year,
                usgsid=query_result_row[5],
                image_name=query_result_row[1],
                metadata_result=metadata_result)

            yield metadata_result
