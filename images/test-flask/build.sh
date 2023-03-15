#!/bin/bash
docker build -t test-flask:3.0.0 \
  --no-cache=true \
  .

