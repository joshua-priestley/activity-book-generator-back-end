#!/bin/sh

export APP_PORT=8080
export MODELS_DIR=./gensim-data 

docker image prune -f
docker-compose up --build --remove-orphans
