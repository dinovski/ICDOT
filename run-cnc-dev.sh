#!/bin/sh

export FLASK_ENV=development
export FLASK_DEBUG=1
export BHOT_CONFIG_FILE=$PWD/bhot-dev.conf
export FLASK_APP=bhot_cnc_runner:app
flask run -p 5002 --eager-loading

: exec gunicorn --reload \
     -e FLASK_ENV=1 -e FLASK_DEBUG=1 \
     -n BHOT-DEV \
     -b :5002 \
     --access-logfile - \
     --error-logfile - \
     bhot_runner:app
