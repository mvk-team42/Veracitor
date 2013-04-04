Veracitor
=========

An application that studies the trust in a network of users, sources
and articles

# Get it running (development mode)

### Step one

Clone the project.

`git clone git@github.com:mvk-team42/Veracitor.git`

### Step two

Install python, setuptools and dependencies.

To get the app running, install a relatively new version of python2
with setuptools. If you use a *NIX based OS, we recommend
[pythonbrew](https://github.com/utahta/pythonbrew) and python 2.7.3.

Afterwards, either use a virtualenv (ex. pythonbrew venv create
team42) or just use pip to install the requirements:

`pip install -r requirements.txt`

### Step three

Install and setup [mongodb](http://www.mongodb.org/).

### Step four

Change settings in `settings.py` and `celeryconf.py` according to your
environment.

### Step five

Start mongod externally.

If you installed the python dependencies in a virtualenv, make sure
you are in your virtualenv now.

##### Celery

Use `python start_celery.py` to start the celery daemon.

The celery worker daemon processes tasks sent out from the web part of
the application.

##### Flask dev webserver

Use `python start_webserver.py` to start the dev webserver.
