
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

### JSON

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



@app.route("/search_producers", methods=["GET","POST"])
def prods():

    if request.method == "POST":
        if request.form:
            f=request.form

            error = ""
            if not f['name']:
                error = "No search parameter."
            elif not f['type']:
                error = "No type chosen."

            if error:
                producers = { "error":error }
            else:
                producers = {}
                #    producers = {'res1':f['name'], 'res2': f['type']}   
                res = extractor.search_producers(possible_prod=f['name'], type_=f['type'])
                for i, x in enumerate(res):
                    x_dict = x.__dict__
                
                    # serialize object id TODO fix
                    x_dict['_data'][None] = default(x_dict['_data'][None])
                    
                    producers["res"+str(i)] = x_dict

            #return json.dumps(producers, cls=JSONEnc)
            return render_template("tabs/search_results.html", producers)
    return redirect(url_for("index"))

@app.route("/")
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
    return render_template("index.html", vera=veracitor)

if __name__ == "__main__":
    app.run()
