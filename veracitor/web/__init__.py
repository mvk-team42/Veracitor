from flask import Flask

# The main flask app object is defined here
app = Flask(__name__)


# Load app settings
try:
    app.config.from_envvar('VERACITOR_SETTINGS')
except:
    app.config.from_pyfile('settings.py')

# Create NetworkModel
try:
    from veracitor.database import *
    app.NetworkModel = globalNetwork.build_network_from_db()
except:
    import sys
    print "Can't build NetworkModel"
    sys.exit(-1)


def runserver():
    "Used to start the webserver."
    if app.config['VERACITOR_PORT']:
        app.run(port=app.config['VERACITOR_PORT'])
    else:
        app.run()

import utils
import jobs
import search
import crawler
import algorithm
import login
#import network
#import ratings
#import account
import index
