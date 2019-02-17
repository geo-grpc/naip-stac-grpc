# STAC + NAIP + gRPC Metadata Service
This is a first version of a [gRPC](https://grpc.io/) service and [protobuf](https://developers.google.com/protocol-buffers/) definition for serving [NAIP](https://registry.opendata.aws/naip/) metadata that tries to be [STAC](https://github.com/radiantearth/stac-spec) compliant.

## TLDR
Requirements:
* `aws` [cli tool](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
* AWS s3 requester pays authorization in ~/.aws/credentials (`aws configure` to setup)
* `ogr2ogr` with postgres extensions
* docker + docker-compose
* [virtualenv](https://virtualenv.pypa.io/en/latest/installation/)

#### Commands
There are two different ways to test the gRPC service. One is with a postgis docker container and the other is with a docker-compose db+service. Both require this initial set of commands.

Initial commands will download a gig or more of shapefiles to your local machine and prepare a database:
```bash
git clone git@github.com:geo-grpc/naip-stac-grpc.git
cd naip-stac-grpc
virtualenv venv
source venv/bin/activate
./download_shapefiles.sh
./naip_import_aws.sh
```

Test version 1; test with the local docker database:
```bash
pip3 install -r requirements.txt
python3 setup.py install
python3 service.py
python3 test_client.py
```

Test version 2; test with docker-compose initialized with a pg_dump file:
```bash
# dump postgres table to file
docker exec naip-metadata-postgis pg_dump -U user -Fc \
  -t naip_visual testdb > ./naip_visual_db-$(date +%Y-%m-%d)
docker stop naip-metadata-postgis
docker-compose up --build -d
# wait for postgres db to initialize. you could omit the `-d` and 
# watch for the initialization completion and execute the rest of 
# the command from another window
sleep 15
docker exec -i naip-stac-grpc_db_1 pg_restore -C --clean --no-acl --no-owner \
  -U user -d testdb < ./naip_visual_db-$(date +%Y-%m-%d)
pip3 install -r requirements.txt
python3 test_client.py
```





## STAC, Protocol Buffers, and gPRC

#### Protobuf Defintions
The definitions for a stac item response are in [`protos/epl/protobuf/stac_item_result.proto`](https://github.com/geo-grpc/naip-stac-grpc/blob/master/protos/epl/protobuf/stac_item_result.proto). It is copied from the protocol buffer for stac defined here:
* https://github.com/geo-grpc/protobuf

There are a couple of distinctions from the STAC definitions. 
* there isn't a properties container on the item result object. It could be added, but for the purposes of the demo it made it more difficult. 
* there isn't a bands array on the item result object.

#### Protobuf Reserved Field Numbers
Protobuf definitions have fields that are indexed by field numbers. As we want people to extend STAC for there own purposes the field numbers 201 to 500 are available for custom definitions. The field numbers from 1 to 200 and from 501 to max are reserved for STAC definitions. More keys could be released as needed.

#### `proto2` vs `proto3`
There are two different versions of the proto file format, `proto2` and `proto3` that are currently in use. For the message response, the `stac_item_result.proto` is defined for `proto2`. In protobuf, messages are like structs. They must have a default value even if that value hasn't been set, and in the name of compactness that value is 0. In proto2, the version 
of our proto file for results, there is a method that allows you to check whether a field has been set (this is absent from `proto3`). That way you can ignore values that are 0, but doesn't represent the data. If the `HasField` method returns false, the data should be ignored. HasField, is a poor name, because there is still a field there is data, it's just the data isn't set by the creator of the message.

#### Geometry 
This stac experiment imports a geometry proto definition used in another gRPC project. One of the aspects of this geometry definition is that you can define your aoi geometry using a wkt, wkb, geojson or esrishape. GeoJSON shouldn't be the only option, especially if a user wants results that are more compact. By default this project returns wkb for compactness, though it can accept wkt or wkb as an input.

## Project Setup 

#### Requirements
install requirements:
```bash
pip3 install -r requirements.txt
```

#### Protoc Compile Step (Optional)
The repo contains compiled python files generated from the included proto file definitions. If you choose to make changes to the proto files you'll need to compile the proto files to python code. The generated code is in the `epl/grpc` and the `epl/protobuf` directories.

```bash
python3 -mgrpc_tools.protoc -I=./protos --python_out=./ \
    ./protos/epl/protobuf/geometry_operators.proto \ 
    ./protos/epl/protobuf/stac.proto
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

To collect all the data data from the AWS NAIP shapefiles (a gig or more) you'll need to execute the included bash script, `naip_import_aws.sh`.

## Testing

Once the `naip_import_aws.sh` script is finished and you have the database up and running you can run the tests. From within the repo directory you can call `pytest` to run all tests. There will be some warnings, from `psycopg2` but beyond that all tests should pass.
```bash
pytest
```

To test the service you can open a terminal and run `python3 service.py` and from another terminal run `python3 test_client.py`, or run the jupyter notebook from the repo.

## Other Docs
STAC is described in further detail here:
* https://github.com/radiantearth/stac-spec
* https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md
* https://github.com/radiantearth/stac-spec/tree/master/extensions/eo
* https://medium.com/radiant-earth-insights/the-state-of-stac-talk-and-sprint-3-recap-cd8eda3b8bdb

gRPC services, protobuf binary, and the proto files that define them can be used separately, but they were designed to be used together for microservices communication. They are part of an open source intiaitive from Google. They're based off of Google's own internal RPC framework, Stubby. More info can be found here:
* https://grpc.io/
* https://grpc.io/docs/quickstart/python.html
* https://developers.google.com/protocol-buffers/

NAIP data:
AWS and ESRI teamed up to provide a bucket on s3 that is requester pays. More information here:
* https://registry.opendata.aws/naip/


