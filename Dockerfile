FROM python:slim

WORKDIR /opt/src/naip-stac-grpc
COPY ./ ./

RUN pip install -r requirements.txt

RUN python -mgrpc_tools.protoc -I=./protos --python_out=./ \
    ./protos/epl/protobuf/geometry.proto \
    ./protos/epl/protobuf/stac.proto
RUN python -mgrpc_tools.protoc -I=./protos --grpc_python_out=./ \
    ./protos/epl/grpc/naip_stac.proto

RUN python setup.py install

CMD python service.py
