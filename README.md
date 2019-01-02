# naip-stac-grpc
demo of STAC + gRPC + NAIP


## Protocol Buffers and gPRC
protocol buffer for stac defined here:
https://github.com/geo-grpc/protobuf

install requirements:
```bash
pip install -r requirements
```

compile protocol buffers
```bash
python3 -mgrpc_tools.protoc -I=./protos --python_out=./ ./protos/epl/protobuf/geometry_operators.proto ./protos/epl/protobuf/stac.proto ./protos/epl/protobuf/stac_item_result.proto 
python3 -mgrpc_tools.protoc -I=./protos --grpc_python_out=./ ./protos/epl/grpc/naip_stac.proto
```

after compiling the proto files included above, install the packages:
```bash
python setup.py install
```

## Postgres Setup
You need an AWS account with s3 requester pays read access. ogr2ogr with Postgres is required for writing data to DB. Docker is required for running the DB.

AWS:
`~/.aws/credentials` with `aws_access_key_id` and `aws_secret_access_key`. NAIP bucket is requester pays.

GDAL + ogr2ogr + postgresql:
```bash
brew install gdal2 --with-postgresql
```

execute the `naip_import_aws.sh` script 

## Testing
