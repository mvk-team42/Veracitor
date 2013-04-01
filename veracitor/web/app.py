
from flask import Flask, render_template, request, redirect, \
                    url_for
from ..database import *

import json
from json import JSONEncoder
from bson.json_util import default

# configuration

app = Flask(__name__)
try:
    app.config.from_envvar('VERACITOR_SETTINGS')
except:
    app.config.from_pyfile('settings.py')

class JSONEnc(JSONEncoder):

    def default(self, o):
        try:
            d = o.__dict__
        except:
            pass
        else:
            return d
        # Let the base class default method raise the TypeError
        return JSONEncoder.default(self, o)

"""
Starts a crawler to crawl the given URL for an entity.

"""
@app.route('/add_entity', methods=['GET','POST'])
def add_entity():

    if request.method == 'POST':
        error = {
            'message' : 'none',
            'type' : 'none'
        }

        if request.form:
            f = request.form

            if not f['url']:
                error = {
                    'message' : 'No source URL specified.',
                    'type' : 'no_url'
                }
        else:
            error = {
                'message' : 'Form data error.',
                'type' : 'form_error'
            }

        return json.dumps({ 'error' : error })

    return redirect(url_for('index'))

"""
Performs a search in the database for producers that match the given
parameters. The client is returned a JSON object with information
about possible errors and computed HTML code representing the result
from the performed search.
"""
@app.route('/search_producers', methods=['GET','POST'])
def search_producers():

    if request.method == 'POST':
        error = {
            'message' : 'none',
            'type' : 'none'
        }
        html = ''

        if request.form:
            f = request.form

            data = {}

            if not f['name']:
                error = {
                    'message' : 'No search parameter.',
                    'type' : 'no_param'
                }
            elif not f['type']:
                error = {
                    'message' : 'No type chosen.',
                    'type' : 'no_type'
                }

            if error['type'] == 'none':
                res = extractor.search_producers(possible_prod=f['name'],
                                                 type_of=f['type'])

                if res:
                    data = { 'result' : res }
                else:
                    error = {
                        'message' : 'Could not find anything.',
                        'type' : 'no_result'
                    }

            if not error['type'] == 'none':
                data = { 'error' : error }

            html = render_template('tabs/search_results.html', data=data)
        else:
            error = {
                'message' : 'Form data error.',
                'type' : 'form_error'
            }

        return json.dumps({ 'error' : error, 'html' : html })

    return redirect(url_for('index'))

@app.route('/')
def index():
    veracitor = {
        'title' : 'Veracitor',
        'tabs' : [
            {
                'name' : 'Search',
                'key' : 'search',
                'viewid' : 'search_view',
                'menuid' : 'search_menu',
                'url' : 'tabs/search_tab.html'
            },
            {
                'name' : 'Network',
                'key' : 'network',
                'viewid' : 'network_view',
                'menuid' : 'network_menu',
                'url' : 'tabs/network_tab.html'
            },
            {
                'name' : 'Ratings',
                'key' : 'ratings',
                'viewid' : 'ratings_view',
                'menuid' : 'ratings_menu',
                'url' : 'tabs/ratings_tab.html'
            },
            {
                'name' : 'Account',
                'key' : 'account',
                'viewid' : 'account_view',
                'menuid' : 'account_menu',
                'url' : 'tabs/account_tab.html'
            }
        ]
    }
    return render_template('index.html', vera=veracitor)

def runserver():
    if app.config['VERACITOR_PORT']:
        app.run(port=app.config['VERACITOR_PORT'])
    else:
        app.run()
