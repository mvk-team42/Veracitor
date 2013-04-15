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
    Caclulates the trust between source and sink in the global network using
    the specified tag.

    .. note::
       This is only used when one only wants to use Tidal Trust. I.e., this is
       not to be used from inside of SUNNY where the tidaltrust module should
       be used directly.

       This function/request operates on the global network (but only by
       reading from it).

    URL Structure:
       /algorithms/tidal_trust?source=SOURCE&sink=SINK&tag=TAG

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

    Errors::
       400 - Bad syntax in request
       405 - Method not allowed

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
