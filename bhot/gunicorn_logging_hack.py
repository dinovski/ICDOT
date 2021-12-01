import logging

"""
This module tries to locate a reasonable log for the Flask application,
when running under gunicorn.

Flask has taken this brain-dead approach:

  Flask does not log messages in production mode by default because it
  does not make any assumptions about your environment
  (http://flask.pocoo.org/docs/errorhandling/). To get Flask's
  app.logger to log messages via gunicorn, you'll have to add a
  logging handler.
  https://github.com/benoitc/gunicorn/issues/379#issuecomment-7904270

But when setting it up to connect to STDERR, it turns out that gunicorn
does not connect its error logs to the underlying flask app. arggg.

Call this function on startup/app-creation (if run directly),
or during first request, like so:

@app.before_first_request
def setup_logging():
    if not app.debug:
        gunicorn_logging_hack(app)


TODO:
Figure out the python/gunicorn/flask logging configuration mess in details,
and use gunicorn's log-config option to log this someplace else.
"""

def gunicorn_logging_hack(app):
    # oh F* python, how I loathe thee, let me count the ways.
    # If we're not running in debug mode, try to find a logger
    # which can actually be used.
    found = None
    for k,v in logging.Logger.manager.loggerDict.items():
        # If gunicorn has a logger, use that for our messages.
        if k == "gunicorn.error":
            found = v
            break

    if not found:
        # Not running under gunicorn (or gunicorn logging not
        # detected) - attach to what I think is STDRR as a fallback
        # (F* me if I know where that is going...)  See:
        # https://github.com/benoitc/gunicorn/issues/379
        found = logging.StreamHandler()

    found.setLevel(logging.DEBUG)
    app.logger.addHandler(found)
    app.logger.setLevel(logging.DEBUG)
