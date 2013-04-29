
from flask import request, redirect, url_for, render_template, abort, jsonify,\
    make_response
from veracitor.web import app
from veracitor.web.utils import store_job_result

import veracitor.tasks.crawler as crawler

### Crawler jobs ###

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
    res = crawler.scrape_article.delay(url)
    store_job_result(res)
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
    store_job_result(res)
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
    store_job_result(res)
    return jsonify(job_id=res.id)
