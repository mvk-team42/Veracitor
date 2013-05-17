

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
        Upon success, returns an object with crawler data, ex::

        {"type":"Newspaper scrape",
         "url":"http://www.dn.se",
         "starttime":"1999-04-04 12:23:34",
         "job_id": "ff92-23ad-232a-2334s-23"}

    Result when finished:
        Object with the created producers name.

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


    res = crawler.scrape_article.delay(url)
    store_job_result(res)
    crawl = create_crawl_dict("Article scrape", url, res.id)
    return jsonify(crawl)


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
        Upon success, returns an object with crawler data, ex::

        {"type":"Newspaper scrape",
         "url":"http://www.dn.se",
         "starttime":"1999-04-04 12:23:34",
         "job_id": "ff92-23ad-232a-2334s-23"}

    Result when finished:
        Object with the created producers name.

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
    store_job_result(res)
    crawl = create_crawl_dict("Newspaper scrape", url, res.id)
    return jsonify(crawl)


@app.route('/jobs/crawler/request_scrape', methods=['GET', 'POST'])
def request_scrape():
    """Requests a scrape from the given URL.

    URL Structure: /jobs/crawler/request_scrape

    Method:
       POST

    Parameters:
       url

    Returns:
        Upon success, returns an object with crawler data, ex::

        {"type":"Newspaper scrape",
         "url":"http://www.dn.se",
         "starttime":"1999-04-04 12:23:34",
         "job_id": "ff92-23ad-232a-2334s-23"}

    Result when finished:
        Object with the created producers name.

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
    store_job_result(res)
    crawl = create_crawl_dict("Newspaper scrape (slower)", url, res.id)
    return jsonify(crawl)

# @app.route('/jobs/crawler/get_crawl_producername', methods=['GET', 'POST'])
# def get_crawl_producername():
#     pass


def create_crawl_dict(crawl_type, url, job_id):
    crawl = {}
    crawl['type'] = crawl_type
    crawl['url'] = url
    crawl['start_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    crawl['job_id'] = job_id

    return crawl