# jobs.py
# =======
# Defines job handling via a RESTful api
# aswell as some utility functions

from flask import request, redirect, url_for, render_template, abort, jsonify
from veracitor.web import app

import veracitor.tasks.crawler as crawler
import veracitor.tasks.algorithms as algorithms

### Crawler jobs ###
    
@app.route('/scrape_article', methods=['POST'])
def scrape_article():
    """
    ## /scrape_article (POST)

    **Description:**
    Starts a crawling job referrable to via job id.

    **URL-Structure:**
    `/scrape_article?url=<url>`

    **Method:**
    POST

    **Parameters:**
    url=<url> a URL-encoded string with the url to be scraped.
    
    **Returns:**
    Upon success, return an object with the job_id, ex:
    
    `{"job_id": "ff92-23ad-232a-2334s-23"}`

    **Errors:**
    400 - Bad syntax in request
    405 - Method not allowed

    **Notes:**

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


@app.route('/add_newspaper', methods=['GET', 'POST'])
def add_newspaper():
    """
    ## /add_newspaper ('GET', 'POST')
    **Description:**
    Starts a crawl of a newspaper.
    **URL-Structure:**

    **Method:**

    **Parameters:**

    **Returns:**

    **Errors:**

    **Notes:**

    """

    pass


@app.route('/request_scrape', methods=['GET', 'POST'])
def request_scrape():
    """
    ## /request_scrape ('GET', 'POST')
    **Description:**
    
    **URL-Structure:**

    **Method:**

    **Parameters:**

    **Returns:**

    **Errors:**

    **Notes:**

    """
    pass

### Algorithm jobs ###

@app.route("/algorithms/tidal_trust", methods=['GET', 'POST'])
def tidal_trust():
    """
    ## /algorithms/tidal_trust ('GET', 'POST')
    **Description:**
    
    **URL-Structure:**

    **Method:**

    **Parameters:**
    required:
        **source** = <_string_> - the name of the source node
        **sink** = <_string_> - the name of the sink node

    optional:
        **tag** = <_string_> - @see veracitor.algorithms.tidaltrust#compute_trust
        **decision** = List of <_string_> - node list with names/ids not to be included
                                             in the trust calculation.
    
    **Returns:**

    **Errors:**

    **Notes:**

    """
    

@app.route("/algorithms/sunny", methods=['GET', 'POST'])
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
    
@app.route("/job_ids", methods=['POST'])
def get_job_ids():
    """
    ## /get_job_ids ('POST'])

    **Description:**
    
    **URL-Structure:**

    **Method:**

    **Parameters:**

    **Returns:**

    **Errors:**

    **Notes:**

    """
    try:
        keys = app.results.keys()
    except AttributeError:
        keys = []

    return jsonify(keys=keys)

@app.route("/job_state/<job_id>", methods=['POST'])
def get_job_state(job_id):
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
        return jsonify(state=str(app.results[job_id].state))
    except:
        abort(404)

@app.route("/job_result", methods=['POST'])
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
