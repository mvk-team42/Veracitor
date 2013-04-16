# jobs.py
# =======
# Defines job handling via a RESTful api
# aswell as some utility functions

"""
.. module:: jobs
    :synopsis: The REST-API of Veracitor defined by jobs.

.. moduleauthor:: Anton Erholt <aerholt@kth.se>
.. moduleauthor:: Daniel Molin <dmol@kth.se>

"""

from flask import request, redirect, url_for, render_template, abort, jsonify
from veracitor.web import app
from veracitor.web.utils import store_job_result

import veracitor.tasks.crawler as crawler
import veracitor.tasks.algorithms as algorithms

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



### Algorithm jobs ###

@app.route("/jobs/algorithms/tidal_trust", methods=['GET', 'POST'])
def tidal_trust():
    """Calculates the trust between source and sink in the global network using
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
        Upon success, returns an object with the job_id, ex::
        {"job_id": "ff92-23ad-232a-2334s-23"}

    Result when finished:
       An object with an object containing the
       results, with keywords trust, threshold, paths_used,
       nodes_used, nodes_unused, source, sink::

       {
          "result":  {
                       "trust": (int),
                       "threshold": (int),
                       "paths_used": (list of lists of str),
                       "nodes_used": (list of str),
                       "nodes_unused": (list of str),
                       "source": (str),
                       "sink": (str),
                       "tag": (str),
          }
       }

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


@app.route("/jobs/algorithms/sunny", methods=['GET', 'POST'])
def sunny():
    """
    Calculates the trust between source and sink in the global network using
    the specified tag.

    URL Structure:
       /jobs/algorithms/sunny

    Method:
       POST

    Parameters:
       source (str): The name of the source node.

       sink (str): The name of the sink node.

       tag (str): A tag name. Only edges/ratings under this tag will be used
       in the trust calculation.

    Returns:
        Upon success, returns an object with the job_id, ex::
        {"job_id": "ff92-23ad-232a-2334s-23"}

    Result when finished:
       See :doc:get_job_result
       An object containing the results, with keywords trust, threshold, paths_used,
       nodes_used, nodes_unused, source, sink::

          {
             "trust": (int);
             "threshold": (int),
             "paths_used": (list of lists of str),
             "nodes_used": (list of str),
             "nodes_unused": (list of str),
             "source": (str),
             "sink": (str),
             "tag": (str),
          }

    Errors::
       400 - Bad syntax in request
       405 - Method not allowed

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

    URL Structure:
       /jobs/job_state

    Method:
        POST

    Parameters:
        job_id (str): The id of the job as a string.

    Returns:
        See <http://docs.celeryproject.org/en/latest/reference/celery.states.html> for more info.
        state (str): The job state, defined as at least the following::
            SUCCESS
            FAILURE
            PENDING


    Errors::
       405 - Method not allowed
       404 - No job with that id.


    """
    if not request.method == 'POST':
        abort(405)
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

    URL Structure:
       /jobs/job_result

    Method:
        POST

    Parameters:
        job_id (str): The id of the job as a string.

    Returns:
       Whatever the corresponding job said it would return under 'Result upon finish',
       stored in an object under the key 'result', ex::

       {
           "result": "scraped article: http://dn.se/nyheter/artikel"
       }


    Errors::
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
        app.logger.debug(res.result)
        return jsonify(result={})
    else:
        return jsonify(result=res.result)
