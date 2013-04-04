from flask import Flask

# The main flask app object is defined here
app = Flask(__name__)


# Load app settings
try:
    app.config.from_envvar('VERACITOR_SETTINGS')
except:
    app.config.from_pyfile('settings.py')



def runserver():
    "Used to start the webserver."
    if app.config['VERACITOR_PORT']:
        app.run(port=app.config['VERACITOR_PORT'])
    else:
        app.run()

import callback
import utils
import search
import network
import ratings
import account
