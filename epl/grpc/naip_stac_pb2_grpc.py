# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from epl.protobuf import stac_item_result_pb2 as epl_dot_protobuf_dot_stac__item__result__pb2
from epl.protobuf import stac_pb2 as epl_dot_protobuf_dot_stac__pb2


class MetadataOperatorsStub(object):
  """
  gRPC Interfaces for working with imagery operators
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Search = channel.unary_stream(
        '/swiftera.grpc.MetadataOperators/Search',
        request_serializer=epl_dot_protobuf_dot_stac__pb2.MetadataRequest.SerializeToString,
        response_deserializer=epl_dot_protobuf_dot_stac__item__result__pb2.MetadataResult.FromString,
        )


class MetadataOperatorsServicer(object):
  """
  gRPC Interfaces for working with imagery operators
  """

  def Search(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_MetadataOperatorsServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Search': grpc.unary_stream_rpc_method_handler(
          servicer.Search,
          request_deserializer=epl_dot_protobuf_dot_stac__pb2.MetadataRequest.FromString,
          response_serializer=epl_dot_protobuf_dot_stac__item__result__pb2.MetadataResult.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'swiftera.grpc.MetadataOperators', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))