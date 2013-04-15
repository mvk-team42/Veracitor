# jobs.py
# =======
# Defines job handling via a RESTful api
# aswell as some utility functions

from flask import request, redirect, url_for, render_template, abort, jsonify
from veracitor.web import app

import veracitor.tasks.crawler as crawler
import veracitor.tasks.algorithms as algorithms

### Crawler jobs ###
    
@app.route('/jobs/crawler/scrape_article', methods=['POST'])
def scrape_article():
    """
    Scrapes an article from a URL and adds it to the database.

    URL Structure:
        /jobs/crawler/scrape_article

    Method:
        POST

    Parameters:
        url (str): A URL to the article which should be scraped.

    Returns:
        Upon success, return an object with the job_id, ex:
        {"job_id": "ff92-23ad-232a-2334s-23"}

    Result when finished:
        result (str) : "scraped article: " + url
    
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
    res = crawler.scrape_article.delay(url)
    store_job_result(res)
    return jsonify(job_id=res.id)


@app.route('/jobs/crawler/add_newspaper', methods=['GET', 'POST'])
def add_newspaper():
    """

    Crawls a URL and adds the newspaper to the database.

    URL Structure:
        /jobs/crawler/add_newspaper

    Method:
        POST

    Parameters:
        url (str): A URL to the newspaper which should be crawled.

    Returns:
        Upon success, return an object with the job_id, ex:
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
    return jsonify(job_id=res.id)


@app.route('/jobs/crawler/request_scrape', methods=['GET', 'POST'])
def request_scrape():
    """
    Requests a scrape from 

    URL Structure:
       /jobs/crawler/request_scrape

    Method:
       POST

    Parameters:
       url

    Returns:
        Upon success, return an object with the job_id, ex::
        {"job_id": "ff92-23ad-232a-2334s-23"}

    Errors::
       400 - Bad syntax in request
       405 - Method not allowed

    """
    pass


### Algorithm jobs ###

@app.route("/jobs/algorithms/tidal_trust", methods=['GET', 'POST'])
def tidal_trust():
    """
    Calculates the trust between source and sink in the global network using
    the specified tag.

    URL Structure:
       /jobs/algorithms/tidal_trust

    Method:
       POST

    Parameters:
       source (str): The name of the source node.

       sink (str): The name of the sink node.

       tag (str): A tag name. Only edges/ratings under this tag will be used
       in the trust calculation.

    Returns:
        Upon success, return an object with the job_id, ex::

        {"job_id": "ff92-23ad-232a-2334s-23"}

    Errors:
       * **400** -- Bad syntax in request
       * **405** -- Method not allowed

    """

    if not request.method == 'POST':
        abort(405)
    try:
        source = request.form['source']
        sink = request.form['sink']
        tag = request.form['tag']
    except KeyError, AttributeError:
        abort(400)

    res = algorithms.tidaltrust.delay(source, sink, tag)
    store_job_result(res)
    return jsonify(job_id=res.id)


@app.route("/jobs/algorithms/sunny", methods=['GET', 'POST'])
def sunny():
    """
    ## /algorithms/sunny ('GET', 'POST')
    **Description:**
    
    **URL-Structure:**

    **Method:**

    **Parameters:**

    **Returns:**

    **Errors:**

    **Notes:**

    """
    pass
    
### Job statistics ###
    
@app.route("/jobs/job_ids", methods=['POST'])
def get_job_ids():
    """
    Returns a list with the current running jobs.

    URL Structure:
       /jobs/job_ids

    Method:
        POST

    Parameters:
        None

    Returns:
        keys (list): A list with the job_ids of the current jobs running.

    Errors::
       405 - Method not allowed

    """
    if not request.method == 'POST':
        abort(405)
    try:
        keys = app.results.keys()
    except AttributeError:
        keys = []

    return jsonify(keys=keys)

@app.route("/jobs/job_state", methods=['POST'])
def get_job_state():
    """
    ## /get_job_state (POST)
    **Description:**
    
    **URL-Structure:**

    **Method:**

    **Parameters:**

    **Returns:**

    **Errors:**
    404 - No job with that id.
    
    **Notes:**

    """
    try:
        job_id = request.form['job_id']
    except:
        abort(404)
    
    try:
        return jsonify(state=str(app.results[job_id].state))
    except:
        abort(404)

@app.route("/jobs/job_result", methods=['POST'])
def get_job_result():
    """
    ## /job_result (POST)
    **Description:**
    
    **URL-Structure:**

    **Method:**

    **Parameters:**

    **Returns:**
    An object containing the
    
    **Errors:**
    405 - Method not allowed.
    404 - No job with that id.
    406 - Job not ready.

    **Notes:**

    """
    if not request.method == 'POST':
        abort(405)
    try:
        res = app.results[request.form['job_id']]
    except:
        abort(404)
    
    if not res.ready():
        abort(406)
    else:
        return jsonify(result=res.result)


### Utils ###

def store_job_result(result):
    """Stores the job result in the app context."""
    if not hasattr(app, 'results'):
        app.results = {}
    if not hasattr(app, 'current_number_of_jobs'):
        app.current_number_of_jobs = 0
    app.results[result.id] = result

    # Here you could add the job id to the session object if the user
    # is logged in.

    app.current_number_of_jobs += 1
