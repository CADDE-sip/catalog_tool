#!/bin/bash

# リリースモードで起動
COMPOSE_HTTP_TIMEOUT=240 docker compose -f docker-compose.yml up -d


