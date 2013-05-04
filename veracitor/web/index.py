# index.py
# ========

"""
.. module:: index
    :synopsis: Defines what should be returned when / is requested.

.. moduleauthor:: John Brynte Turesson <johntu@kth.se>
.. moduleauthor:: Anton Erholt <aerholt@kth.se>

"""

from flask import render_template, url_for, session

from veracitor.web import app, utils
from veracitor.database import *



#app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='images/favicon.ico'))

@app.route('/')
def index():
    """
    Initializes the web page.
    """

        
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
