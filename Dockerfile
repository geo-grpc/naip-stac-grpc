FROM python:slim

COPY ./ ./

RUN pip install -r requirements.txt

RUN python setup.py install

CMD python service.py
