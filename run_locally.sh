#!/bin/sh

export APP_PORT=8080

docker image prune -f
docker-compose up --build --remove-orphans
