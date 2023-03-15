FROM python:3.7
ADD . /code
EXPOSE 8080
WORKDIR /code
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt
CMD ["python3", "-m", "swagger_server"]