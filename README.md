# naip-stac-grpc
demo of STAC + gRPC + NAIP


## Protocol Buffers and gPRC
protocol buffer for stac defined here:
https://github.com/geo-grpc/protobuf

compile protocol buffers
```bash
python3 -mgrpc_tools.protoc -I=./protos --python_out=./ ./protos/epl/protobuf/geometry_operators.proto ./protos/epl/protobuf/stac.proto
```