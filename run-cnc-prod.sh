#!/bin/sh

export FLASK_ENV=production
export FLASK_DEBUG=0
export BHOT_CONFIG_FILE=$PWD/bhot-prod.conf
export FLASK_APP=bhot_cnc_runner:app
: flask run -p 5002 --eager-loading

exec gunicorn --reload \
     -e FLASK_ENV=production -e FLASK_DEBUG=0 \
     -n ICDOT-PROD \
     -b :5012 \
     --access-logfile - \
     --error-logfile - \
     bhot_cnc_runner:app
