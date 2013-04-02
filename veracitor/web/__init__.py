from flask import Flask

app = Flask(__name__)
try:
    app.config.from_envvar('VERACITOR_SETTINGS')
except:
    app.config.from_pyfile('settings.py')

def runserver():
    if app.config['VERACITOR_PORT']:
        app.run(port=app.config['VERACITOR_PORT'])
    else:
        app.run()

import utils
import search
import network
import ratings
import account
