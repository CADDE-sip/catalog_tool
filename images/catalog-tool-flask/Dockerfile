FROM python:3.9.12-alpine3.15
ADD . /code
WORKDIR /code
RUN apk add gcc g++ linux-headers
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt
#CMD ["python", "app.py"]
