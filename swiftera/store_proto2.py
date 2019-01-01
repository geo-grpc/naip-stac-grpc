from epl.protobuf import stac_proto2_pb2
from epl.protobuf import stac_pb2 as stac
from swiftera.store import PostgresStore
from datetime import datetime, date, timezone
from typing import Tuple, List
from collections import namedtuple
from google.protobuf.descriptor import FieldDescriptor
from google.protobuf.timestamp_pb2 import Timestamp
from geoalchemy2.elements import WKTElement, WKBElement
import calendar

_type_dict = {v: k for k, v in vars(FieldDescriptor).items() if k.startswith('TYPE_')}

Repeated = namedtuple('Repeated', ['value'])
Map = namedtuple('Map', ['key', 'value'])


def _field_type(field, context):
    """Helper that returns either a str or nametuple corresponding to the field type"""
    if field.message_type is not None:
        return message_as_namedtuple(field.message_type, context)
    else:
        return _type_dict[field.type]


def field_type(field, context):
    """Returns the protobuf type for a given field descriptor
    A Repeated, Map, or str object may be returned. Strings correspond to protobuf types.
    """
    if field.label == FieldDescriptor.LABEL_REPEATED:
        msg_type = field.message_type
        is_map = msg_type is not None and msg_type.GetOptions().map_entry
        if is_map:
            key = _field_type(field.message_type.fields[0], context)
            value = _field_type(field.message_type.fields[1], context)
            return Map(key, value)
        else:
            value = _field_type(field, context)
            return Repeated(value)
    else:
        return _field_type(field, context)


def message_as_namedtuple(descr, context):
    """Returns a namedtuple corresponding to the given message descriptor"""
    name = descr.name
    if name not in context:
        Msg = namedtuple(name, [f.name for f in descr.fields])
        context[name] = Msg(*(field_type(f, context) for f in descr.fields))
    return context[name]


def module_msgs(module):
    """Returns a dict of {message name: namedtuple} from a given protobuf module"""
    context = dict()
    return {k: message_as_namedtuple(v, context)
            for k, v in module.DESCRIPTOR.message_types_by_name.items()}


def is_message(field):
    """Helper that returns True if a field is a custom message type"""
    return isinstance(field, tuple)


def timestamp_from_datetime(dt):
    ts = Timestamp()

    if isinstance(dt, date):
        ts.seconds = calendar.timegm(dt.timetuple())
    else:
        ts.seconds = dt.replace(tzinfo=timezone.utc).timestamp()

    return ts


def query_to_metadata(query_result_row: Tuple, headers: List, postgres_connection):
    context = dict()
    message_as_namedtuple(stac_proto2_pb2.DESCRIPTOR.message_types_by_name['MetadataResult'], context)

    metadata_results = stac_proto2_pb2.MetadataResult()
    for index, item in enumerate(query_result_row):
        db_key = headers[index]
        if db_key not in postgres_connection.db_message_map:
            continue

        message_key = postgres_connection.db_message_map[db_key]
        field_name = metadata_results.DESCRIPTOR.fields_by_name[message_key].name

        proto_type = getattr(context['MetadataResult'], field_name)
        if isinstance(proto_type, str):
            setattr(metadata_results, message_key, item)
        elif context['Timestamp'] == proto_type:
            value = getattr(metadata_results, message_key)
            value.CopyFrom(timestamp_from_datetime(item))
        elif context['GeometryBagData'] == proto_type:
            value = getattr(metadata_results, message_key)
            if isinstance(item, WKBElement):
                value.wkb.append(bytes(item.data))
            elif isinstance(item, WKTElement):
                value.wkt.append(item.data)
            else:
                raise Exception("geometry type not defined")
            # TODO if there's a spatial reference should be added to data
        elif context['BBoxField'] == proto_type:
            print('BBoxField')

    return metadata_results