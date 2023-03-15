FROM python:3.9.12-alpine3.15
ADD . /code
#EXPOSE 50051
WORKDIR /code

RUN apk add --no-cache alpine-sdk musl-dev libffi-dev mariadb-connector-c-dev
RUN apk add musl linux-headers gcc g++ make gfortran openblas-dev python3 python3-dev
RUN apk add --update gfortran linux-headers

RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt
CMD ["python", "demo.py"]

