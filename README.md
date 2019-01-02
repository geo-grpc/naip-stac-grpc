# naip-stac-grpc
demo of STAC + gRPC + NAIP

## STAC, Protocol Buffers, and gPRC
The definitions for a stac item response are in [`protos/epl/protobuf/stac_item_result.proto`](https://github.com/geo-grpc/naip-stac-grpc/blob/master/protos/epl/protobuf/stac_item_result.proto). It is copied from the protocol buffer for stac defined here:
https://github.com/geo-grpc/protobuf

## Project Setup 

#### Requirements
install requirements:
```bash
pip3 install -r requirements
```

#### Protoc Compile Step (Optional)
The repo contains compiled python files generated from the included proto file definitions. If you choose to make changes to the proto files you'll need to compile the proto files to python code. The generated code is in the `epl/grpc` and the `epl/protobuf` directories.

```bash
python3 -mgrpc_tools.protoc -I=./protos --python_out=./ \
    ./protos/epl/protobuf/geometry_operators.proto ./protos/epl/protobuf/stac.proto \
    ./protos/epl/protobuf/stac_item_result.proto 
python3 -mgrpc_tools.protoc -I=./protos --grpc_python_out=./ \
    ./protos/epl/grpc/naip_stac.proto
```

#### Install Packages
after compiling the proto files included above , install the packages:
```bash
python3 setup.py install
```

#### Postgres Setup
You need an AWS account with s3 requester pays read access. `ogr2ogr` with Postgres plugin is required for writing data to DB. Docker is required for running the DB.

AWS Setup:
`~/.aws/credentials` with `aws_access_key_id` and `aws_secret_access_key`. NAIP bucket is requester pays.

GDAL + ogr2ogr + postgresql:
```bash
brew install gdal2 --with-postgresql
```

To collect all the data data from the AWS NAIP shapefiles you'll need to execute the included bash script, `naip_import_aws.sh`.

## Testing

Once the `naip_import_aws.sh` script is finished and you have the database up and running you can run the tests. From within the repo directory you can call `pytest` to run all tests. There will be some warnings, from `psycopg2` but beyond that all tests should pass.
```bash
pytest
```

To test the service you can open a terminal and run `python3 service.py` and from another terminal run `python3 test_client.py`, or run the jupyter notebook from the repo.


