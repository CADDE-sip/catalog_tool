#!/bin/bash
docker build -t authentication_oauth2 \
  --no-cache=true \
  --build-arg HTTP_PROXY=$1 \
  --build-arg HTTPS_PROXY=$1 \
  --build-arg http_proxy=$1 \
  --build-arg https_proxy=$1 \
  .
