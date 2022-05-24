icdot
====

Data collection from participating transplant centers.

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter
     :target: https://github.com/cookiecutter/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style

:License: GPLv3

Development
-----------

Learn how to develop locally_ on this project.

.. _locally: https://cookiecutter-django.readthedocs.io/en/latest/developing-locally-docker.html

All of the documentation below applies, but when using docker-compose things will look like this::

    $ docker-compose -f local.yml up
    $ docker-compose -f local.yml run --rm django python manage.py createsuperuser
    $ docker-compose -f local.yml run --rm django
    $ docker-compose -f local.yml run --rm django bash -c "coverage run -m pytest -s -v && coverage report -m"


If you need access to a debugger, for example when using `ipdb` you should use `... run --service-ports ...`.


What is `pre-commit`
^^^^^^^^^^^^^^^^^^^

When you made some changes you will need to git commit them. This project uses `pre-commit` to ensure everything is okay before creating a commit. When this is happening you might get an error about `pre-commit` not being installed. This hapens if you have not installed the project locally and have _only_ been relying on the docker environement.

Check `pre-commit`'s documentation_ but one way of installing it locally is:

.. _documentation: https://pre-commit.com/#install

::

    $ python3.9 -m venv venv
    $ source venv/bin/activate
    $ pre-commit install


How to update models
^^^^^^^^^^^^^^^^^^^^

Adding fields to models happens by first editing `<icdot/transplants/models/>`_.

Then don't forget to build the migrations::

  $ docker-compose -f local.yml run --rm django python manage.py makemigrations

And once you've tested and are happy with that you can commit it::

  $ git add icdot/ransplants/migrations/


Settings
--------

Moved to settings_.

.. _settings: http://cookiecutter-django.readthedocs.io/en/latest/settings.html

Basic Commands
--------------

Setting Up Your Users
^^^^^^^^^^^^^^^^^^^^^

* To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

* To create an **superuser account**, use this command::

    $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy icdot

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest

Live reloading and Sass CSS compilation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Moved to `Live reloading and SASS compilation`_.

.. _`Live reloading and SASS compilation`: http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html

Email Server
^^^^^^^^^^^^

In development, it is often nice to be able to see emails that are being sent from your application. For that reason local SMTP server `MailHog`_ with a web interface is available as docker container.

Container mailhog will start automatically when you will run all docker containers.
Please check `cookiecutter-django Docker documentation`_ for more details how to start all containers.

With MailHog running, to view messages that are sent by your application, open your browser and go to ``http://127.0.0.1:8025``

.. _mailhog: https://github.com/mailhog/MailHog

Deployment
----------

The following details how to deploy this application.

Docker
^^^^^^

See detailed `cookiecutter-django Docker documentation`_.

.. _`cookiecutter-django Docker documentation`: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html
