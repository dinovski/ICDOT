#!/bin/sh

export FLASK_ENV=production
export FLASK_DEBUG=0
export BHOT_CONFIG_FILE=$PWD/bhot-prod.conf
export FLASK_APP=bhot_runner:app

exec gunicorn --reload \
     -n BHOT-PROD \
     -b :5010 \
     --access-logfile - \
     --error-logfile - \
     bhot_runner:app
