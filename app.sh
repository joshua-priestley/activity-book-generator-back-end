#!/bin/sh

export FLASK_APP=activitygen
export FLASK_ENV=development

python -m flask run --host=0.0.0.0
