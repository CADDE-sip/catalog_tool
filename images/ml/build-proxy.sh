#!/bin/bash
docker build -t machine-learn \
  --no-cache=true \
  --build-arg HTTP_PROXY=$1 \
  --build-arg HTTPS_PROXY=$1 \
  --build-arg http_proxy=$1 \
  --build-arg https_proxy=$1 \
  .
