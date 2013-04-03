Veracitor
=========

An application that studies the trust in a network of users, sources and articles

# Get it running

### Step one

Clone the project.

`git clone git@github.com:mvk-team42/Veracitor.git`

### Step two

Install python, setuptools and dependencies.

To get the app running, install a relatively new version of python2 with setuptools.
If you use a *NIX based OS, we recommend [pythonbrew](https://github.com/utahta/pythonbrew) and python 2.7.3.

Afterwards, either use a virtualenv (ex. pythonbrew venv create team42) or just use pip
to install the requirements:

`pip install -r requirements.txt`

### Step three

Install and setup [mongodb](http://www.mongodb.org/).

### Step four

Run celery
