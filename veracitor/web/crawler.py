

""" 
.. module:: crawler
    :synopsis: 

.. moduleauthor:: Anton Erholt <aerholt@kth.se>
.. moduleauthor:: John Brynte Turesson <johntu@kth.se>
"""


from flask import request, redirect, url_for, render_template, abort, jsonify,\
    make_response, session
from veracitor.web import app
from veracitor.web.utils import store_job_result

import veracitor.tasks.crawler as crawler
import datetime

### Crawler jobs ###

# TODO:

# This should probably be more tied to the user and
# perhaps logged more thoroughly.

# The crawls are currently saved in the current session, but should
# probably be stored in the database when enhancing.

# The crawls stored in session are currently removed on logout. See
# login.py - logout.

@app.route('/jobs/crawler/scrape_article', methods=['GET', 'POST'])
def scrape_article():
    """Scrapes an article from a URL and adds it to the database.

    URL Structure:
        ``/jobs/crawler/scrape_article``

    Method:
        POST

    Parameters:
        url (str): A URL to the article which should be scraped.

    Returns:
        Upon success, returns an object with the job_id, ex::

        {"job_id": "ff92-23ad-232a-2334s-23"}

    Result when finished:
        *result (str)* : "scraped article: " + url

    Errors:
       * **400** -- Bad syntax in request
       * **405** -- Method not allowed

    """
    if not request.method == 'POST':
        abort(405)
    try:
        url = request.form['url']
    except KeyError, AttributeError:
        abort(400)

    
    crawls =  session.get('crawls')
    if crawls == None:
        crawls = {}

    res = crawler.scrape_article.delay(url)

    crawl = {}
    crawl['type'] = "Article scrape"
    crawl['url'] = url
    crawl['start_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    crawls[res.id] = crawl

    store_job_result(res)

    session['crawls'] = crawls
    return jsonify(job_id=res.id)


@app.route('/jobs/crawler/add_newspaper', methods=['GET', 'POST'])
def add_newspaper():
    """Crawls a URL and adds the newspaper to the database.

    URL Structure:
        /jobs/crawler/add_newspaper

    Method:
        POST

    Parameters:
        url (str): A URL to the newspaper which should be crawled.

    Returns:
        Upon success, returns an object with the job_id, ex::
        {"job_id": "ff92-23ad-232a-2334s-23"}

    Result when finished:
        result (str) : "requested scrape for: " + url

    Errors::
       400 - Bad syntax in request
       405 - Method not allowed

    """
    if not request.method == 'POST':
        abort(405)
    try:
        url = request.form['url']
    except KeyError, AttributeError:
        abort(400)
    res = crawler.add_newspaper.delay(url)

    crawls =  session.get('crawls')
    if crawls == None:
        crawls = {}

    crawl = {}
    crawl['type'] = "Newspaper scrape"
    crawl['url'] = url
    crawl['start_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    crawls[res.id] = crawl

    store_job_result(res)
    session['crawls'] = crawls
    
    return jsonify(job_id=res.id)


@app.route('/jobs/crawler/request_scrape', methods=['GET', 'POST'])
def request_scrape():
    """Requests a scrape from the given URL.

    URL Structure: /jobs/crawler/request_scrape

    Method:
       POST

    Parameters:
       url

    Returns:
        Upon success, returns an object with the job_id, ex::
        {"job_id": "ff92-23ad-232a-2334s-23"}

    Errors::
       400 - Bad syntax in request
       405 - Method not allowed

    """
    if not request.method == 'POST':
        abort(405)
    try:
        url = request.form['url']
    except KeyError, AttributeError:
        abort(400)
    res = crawler.request_scrape.delay(url)

    crawls =  session.get('crawls')
    if crawls == None:
        crawls = {}

    crawl = {}
    crawl['type'] = "Newspaper scrape"
    crawl['url'] = url
    crawl['start_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    crawls[res.id] = crawl
    
    store_job_result(res)
    session['crawls'] = crawls
    return jsonify(job_id=res.id)


@app.route("/jobs/crawler/crawls", methods=["POST"])
def get_crawls():
    """Returns data of the users currently running crawler jobs.

    URL Structure: /jobs/crawler/crawls

    Method:
       POST

    Parameters:
       None

    Returns:
        Upon success, returns an object with the job_id, ex::
        {"job_id": "ff92-23ad-232a-2334s-23"}

    Errors::
       204 - No Content, no crawls started
       405 - Method not allowed

    """
    if not request.method == 'POST':
        abort(405)

    crawls =  session.get('crawls')
    if crawls == None:
        return make_response('', 204)
    else:
        return jsonify(session.get('crawls'))

