import os,sys,io
from configobj import ConfigObj
from pprint import pprint

config_filename = os.environ.get('BHOT_CONFIG_FILE',"")
if len(config_filename)==0:
    sys.exit("BHOT_CONFIG_FILE environment variable not set")


config = ConfigObj(config_filename,
                   raise_errors=True,file_error=True)

#TODO: verify certain sections exists, to avoid confusing python "keyError" exceptions.


flask_config = config['flask']

## Ugly Hack to convert string values (from INI file)
## to other python types. In python 2 it "just worked" without type conversions...

force_int_values = ['MAX_CONTENT_LENGTH']
for v in force_int_values:
    if v in flask_config:
        try:
            flask_config[v] = flask_config.as_int(v)
        except ValueError:
            sys.exit("config error: key '%s' value '%s' is not integer" % (v, flask_config[v]))


force_bool_values = ['SQLALCHEMY_TRACK_MODIFICATIONS','SQLALCHEMY_ECHO',
                     'DEBUG_TB_INTERCEPT_REDIRECTS']
for v in force_bool_values:
    if v in flask_config:
        try:
            flask_config[v] = flask_config.as_bool(v)
        except ValueError:
            sys.exit("config error: key '%s' value '%s' is not boolean" % (v, flask_config[v]))
