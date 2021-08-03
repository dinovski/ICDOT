#!/bin/sh

export FLASK_ENV=development
export FLASK_DEBUG=1
export BHOT_CONFIG_FILE=$PWD/bhot-dev.conf
export FLASK_APP=bhot_runner:app
flask run --eager-loading

: exec gunicorn --reload \
     -e FLASK_ENV=1 -e FLASK_DEBUG=1 \
     -n BHOT-DEV \
     -b :5000 \
     --access-logfile - \
     --error-logfile - \
     bhot_runner:app
