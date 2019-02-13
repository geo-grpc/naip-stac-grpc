FROM python:slim

WORKDIR /opt/src/naip-stac-grpc
COPY ./ ./

RUN pip install -r requirements.txt

RUN python setup.py install

CMD python service.py
