#!/bin/sh

export APP_PORT=8080
export MODELS_DIR=./gensim-data 
export NOUN_PROJECT_API_KEY=
export NOUN_PROJECT_API_SECRET=
export WORDS_API_URL="http://cloud-vm-43-108.doc.ic.ac.uk"

docker image prune -f
docker-compose up --build --remove-orphans
