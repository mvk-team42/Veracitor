
from flask import Flask, render_template, request, redirect, \
                    url_for
from ..database import *
import json

# configuration

app = Flask(__name__)
try:
    app.config.from_envvar('VERACITOR_SETTINGS')
except:
    app.config.from_pyfile('settings.py')


@app.route("/search_producers", methods=["GET","POST"])
def prods():
    print request

    if request.method == "POST":
        if request.form:
            f=request.form
            
            error = None
            if not f['name']:
                error = "No search parameter."
            elif not f['type']:
                error = "No type chosen."
                
            if error:
                return "ERROR: "+error
             
            producers = {'res1':f['name'], 'res2': f['type']}   
            #producers = search_producers(f['name'], f['type'])
            return json.dumps(producers)
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
