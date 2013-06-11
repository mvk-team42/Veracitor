Veracitor
=========

An application that studies the trust in a network of users, sources
and articles.


# Source & documentation

### Source
Veracitor source is split into several packages inside the main package.
The following package-structure is kept:

    \veracitor
             \_web
             \_crawler
             \_algorithms
             \_tasks
             \_database

### Documentation

The entire project is documented on a per-package level.


# Installation

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
environment. Add the environment variable VERACITOR_SETTINGS to your
env. Make sure it contains the absolute path to the settings file.

Example:
Ubuntu Linux - append this to `~/.bashrc` :

    export VERACITOR_SETTINGS="/path/to/Veracitor/settings.py"

Don't forget to also activate your settings ex. :

    source ~/.bashrc


### Step five

Start mongod externally.

If you installed the python dependencies in a virtualenv, make sure
you are in your virtualenv now.

##### Celery

Use `celery -A veracitor.tasks.tasks.taskmgr worker -l INFO -B`
to start the celery daemon from the Veracitor folder.

The celery worker daemon processes tasks sent out from the web part of
the application.

By default the celeryd saves the results in a mongodb called
`celery_db`, in a collection called `veracitor_taskmeta_collection`.
This collection may need to be cleared after a while, see Issue #23
(unless the celery beat is functioning).

##### Flask dev webserver

Use `python start_webserver.py` to start the dev webserver from the
Veracitor folder.

##### Misc

This prototype has been developed at a dev-server. For convenience,
SSH has been used to tunnel the web traffic like this:

    ssh user@dev.server.ip.or.dns.com -L [local_port]:localhost:[web_server_port]

Which makes the website visible by surfing to http://localhost:localport/ .