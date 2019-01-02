# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: epl/protobuf/stac_item_result.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from epl.protobuf import geometry_operators_pb2 as epl_dot_protobuf_dot_geometry__operators__pb2
from epl.protobuf import stac_pb2 as epl_dot_protobuf_dot_stac__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='epl/protobuf/stac_item_result.proto',
  package='epl.protobuf',
  syntax='proto2',
  serialized_options=_b('\n\025com.epl.protobuf.stacB\014StacMetadataP\001\242\002\003STC'),
  serialized_pb=_b('\n#epl/protobuf/stac_item_result.proto\x12\x0c\x65pl.protobuf\x1a\x1fgoogle/protobuf/timestamp.proto\x1a%epl/protobuf/geometry_operators.proto\x1a\x17\x65pl/protobuf/stac.proto\"\x9c\x01\n\x0b\x42\x61ndDetails\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0b\x63ommon_name\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x0b\n\x03gsd\x18\x04 \x01(\x02\x12\x10\n\x08\x61\x63\x63uracy\x18\x05 \x01(\x02\x12\x19\n\x11\x63\x65nter_wavelength\x18\x06 \x01(\x02\x12\x1b\n\x13\x66ull_width_half_max\x18\x07 \x01(\x02\"\xda\x01\n\x05\x41sset\x12\x0c\n\x04href\x18\x01 \x01(\t\x12,\n\nasset_type\x18\x02 \x01(\x0e\x32\x18.epl.protobuf.ASSET_TYPE\x12&\n\x07\x65o_band\x18\x03 \x01(\x0e\x32\x15.epl.protobuf.EO_BAND\x12,\n\x10\x62ucket_iaas_host\x18\x04 \x01(\x0e\x32\x12.epl.protobuf.IAAS\x12\x14\n\x0c\x62ucket_owner\x18\x05 \x01(\t\x12\x15\n\rbucket_region\x18\x06 \x01(\t\x12\x12\n\nbucket_ref\x18\x07 \x01(\t\"\xe8\x04\n\x0eMetadataResult\x12\n\n\x02id\x18\x01 \x01(\t\x12.\n\x0b\x65o_platform\x18\x02 \x01(\x0e\x32\x19.epl.protobuf.EO_PLATFORM\x12\x32\n\reo_instrument\x18\x03 \x01(\x0e\x32\x1b.epl.protobuf.EO_INSTRUMENT\x12\x0f\n\x07\x65o_epsg\x18\x04 \x01(\r\x12\x38\n\x06\x61ssets\x18\x06 \x03(\x0b\x32(.epl.protobuf.MetadataResult.AssetsEntry\x12\x16\n\x0e\x65o_sun_azimuth\x18\x08 \x01(\x02\x12\x18\n\x10\x65o_sun_elevation\x18\t \x01(\x02\x12\x0e\n\x06\x65o_gsd\x18\n \x01(\x02\x12\x14\n\x0c\x65o_off_nadir\x18\x0b \x01(\x02\x12\x12\n\neo_azimuth\x18\x0c \x01(\x02\x12\x16\n\x0e\x65o_cloud_cover\x18\r \x01(\x02\x12(\n\x04\x62\x62ox\x18\x0e \x01(\x0b\x32\x1a.epl.protobuf.EnvelopeData\x12/\n\x08geometry\x18\x0f \x01(\x0b\x32\x1d.epl.protobuf.GeometryBagData\x12\'\n\x08\x65o_bands\x18\x10 \x01(\x0e\x32\x15.epl.protobuf.EO_BAND\x12\x31\n\x0csrc_img_date\x18\xc9\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x0f\n\x06usgsid\x18\xca\x01 \x01(\t\x1a\x42\n\x0b\x41ssetsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\"\n\x05value\x18\x02 \x01(\x0b\x32\x13.epl.protobuf.Asset:\x02\x38\x01J\x04\x08\x05\x10\x06J\x05\x08\x11\x10\xc9\x01\x42-\n\x15\x63om.epl.protobuf.stacB\x0cStacMetadataP\x01\xa2\x02\x03STC')
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,epl_dot_protobuf_dot_geometry__operators__pb2.DESCRIPTOR,epl_dot_protobuf_dot_stac__pb2.DESCRIPTOR,])




_BANDDETAILS = _descriptor.Descriptor(
  name='BandDetails',
  full_name='epl.protobuf.BandDetails',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='epl.protobuf.BandDetails.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='common_name', full_name='epl.protobuf.BandDetails.common_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='description', full_name='epl.protobuf.BandDetails.description', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='gsd', full_name='epl.protobuf.BandDetails.gsd', index=3,
      number=4, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='accuracy', full_name='epl.protobuf.BandDetails.accuracy', index=4,
      number=5, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='center_wavelength', full_name='epl.protobuf.BandDetails.center_wavelength', index=5,
      number=6, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='full_width_half_max', full_name='epl.protobuf.BandDetails.full_width_half_max', index=6,
      number=7, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=151,
  serialized_end=307,
)


_ASSET = _descriptor.Descriptor(
  name='Asset',
  full_name='epl.protobuf.Asset',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='href', full_name='epl.protobuf.Asset.href', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='asset_type', full_name='epl.protobuf.Asset.asset_type', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='eo_band', full_name='epl.protobuf.Asset.eo_band', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bucket_iaas_host', full_name='epl.protobuf.Asset.bucket_iaas_host', index=3,
      number=4, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bucket_owner', full_name='epl.protobuf.Asset.bucket_owner', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bucket_region', full_name='epl.protobuf.Asset.bucket_region', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bucket_ref', full_name='epl.protobuf.Asset.bucket_ref', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=310,
  serialized_end=528,
)


_METADATARESULT_ASSETSENTRY = _descriptor.Descriptor(
  name='AssetsEntry',
  full_name='epl.protobuf.MetadataResult.AssetsEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='epl.protobuf.MetadataResult.AssetsEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='epl.protobuf.MetadataResult.AssetsEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1068,
  serialized_end=1134,
)

_METADATARESULT = _descriptor.Descriptor(
  name='MetadataResult',
  full_name='epl.protobuf.MetadataResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='epl.protobuf.MetadataResult.id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='eo_platform', full_name='epl.protobuf.MetadataResult.eo_platform', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='eo_instrument', full_name='epl.protobuf.MetadataResult.eo_instrument', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='eo_epsg', full_name='epl.protobuf.MetadataResult.eo_epsg', index=3,
      number=4, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='assets', full_name='epl.protobuf.MetadataResult.assets', index=4,
      number=6, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='eo_sun_azimuth', full_name='epl.protobuf.MetadataResult.eo_sun_azimuth', index=5,
      number=8, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='eo_sun_elevation', full_name='epl.protobuf.MetadataResult.eo_sun_elevation', index=6,
      number=9, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='eo_gsd', full_name='epl.protobuf.MetadataResult.eo_gsd', index=7,
      number=10, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='eo_off_nadir', full_name='epl.protobuf.MetadataResult.eo_off_nadir', index=8,
      number=11, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='eo_azimuth', full_name='epl.protobuf.MetadataResult.eo_azimuth', index=9,
      number=12, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='eo_cloud_cover', full_name='epl.protobuf.MetadataResult.eo_cloud_cover', index=10,
      number=13, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bbox', full_name='epl.protobuf.MetadataResult.bbox', index=11,
      number=14, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='geometry', full_name='epl.protobuf.MetadataResult.geometry', index=12,
      number=15, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='eo_bands', full_name='epl.protobuf.MetadataResult.eo_bands', index=13,
      number=16, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='src_img_date', full_name='epl.protobuf.MetadataResult.src_img_date', index=14,
      number=201, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='usgsid', full_name='epl.protobuf.MetadataResult.usgsid', index=15,
      number=202, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_METADATARESULT_ASSETSENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=531,
  serialized_end=1147,
)

_ASSET.fields_by_name['asset_type'].enum_type = epl_dot_protobuf_dot_stac__pb2._ASSET_TYPE
_ASSET.fields_by_name['eo_band'].enum_type = epl_dot_protobuf_dot_stac__pb2._EO_BAND
_ASSET.fields_by_name['bucket_iaas_host'].enum_type = epl_dot_protobuf_dot_stac__pb2._IAAS
_METADATARESULT_ASSETSENTRY.fields_by_name['value'].message_type = _ASSET
_METADATARESULT_ASSETSENTRY.containing_type = _METADATARESULT
_METADATARESULT.fields_by_name['eo_platform'].enum_type = epl_dot_protobuf_dot_stac__pb2._EO_PLATFORM
_METADATARESULT.fields_by_name['eo_instrument'].enum_type = epl_dot_protobuf_dot_stac__pb2._EO_INSTRUMENT
_METADATARESULT.fields_by_name['assets'].message_type = _METADATARESULT_ASSETSENTRY
_METADATARESULT.fields_by_name['bbox'].message_type = epl_dot_protobuf_dot_geometry__operators__pb2._ENVELOPEDATA
_METADATARESULT.fields_by_name['geometry'].message_type = epl_dot_protobuf_dot_geometry__operators__pb2._GEOMETRYBAGDATA
_METADATARESULT.fields_by_name['eo_bands'].enum_type = epl_dot_protobuf_dot_stac__pb2._EO_BAND
_METADATARESULT.fields_by_name['src_img_date'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
DESCRIPTOR.message_types_by_name['BandDetails'] = _BANDDETAILS
DESCRIPTOR.message_types_by_name['Asset'] = _ASSET
DESCRIPTOR.message_types_by_name['MetadataResult'] = _METADATARESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

BandDetails = _reflection.GeneratedProtocolMessageType('BandDetails', (_message.Message,), dict(
  DESCRIPTOR = _BANDDETAILS,
  __module__ = 'epl.protobuf.stac_item_result_pb2'
  # @@protoc_insertion_point(class_scope:epl.protobuf.BandDetails)
  ))
_sym_db.RegisterMessage(BandDetails)

Asset = _reflection.GeneratedProtocolMessageType('Asset', (_message.Message,), dict(
  DESCRIPTOR = _ASSET,
  __module__ = 'epl.protobuf.stac_item_result_pb2'
  # @@protoc_insertion_point(class_scope:epl.protobuf.Asset)
  ))
_sym_db.RegisterMessage(Asset)

MetadataResult = _reflection.GeneratedProtocolMessageType('MetadataResult', (_message.Message,), dict(

  AssetsEntry = _reflection.GeneratedProtocolMessageType('AssetsEntry', (_message.Message,), dict(
    DESCRIPTOR = _METADATARESULT_ASSETSENTRY,
    __module__ = 'epl.protobuf.stac_item_result_pb2'
    # @@protoc_insertion_point(class_scope:epl.protobuf.MetadataResult.AssetsEntry)
    ))
  ,
  DESCRIPTOR = _METADATARESULT,
  __module__ = 'epl.protobuf.stac_item_result_pb2'
  # @@protoc_insertion_point(class_scope:epl.protobuf.MetadataResult)
  ))
_sym_db.RegisterMessage(MetadataResult)
_sym_db.RegisterMessage(MetadataResult.AssetsEntry)


DESCRIPTOR._options = None
_METADATARESULT_ASSETSENTRY._options = None
# @@protoc_insertion_point(module_scope)
