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

from flask import request, redirect, url_for, render_template, abort, jsonify,\
    make_response
from veracitor.web import app

log = app.logger.debug

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

    Success::
       200 - OK (job done)
       204 - No Content (job not done)
    Errors::
       405 - Method not allowed.
       404 - No job with that id.

    **Notes:**

    """
    if not request.method == 'POST':
        abort(405)
    try:
        res = app.results[request.form['job_id']]
        log(res)
    except Exception, err:
        abort(404)

    if not res.ready():
        return make_response('', 204)
    elif not res.result.get('template_url') == None:
        try:
            res.result['html'] = render_template(res.result['template_url'], 
                                                 data=res.result['data'])
        except KeyError:
            raise Exception('Couldn\'t parse template.')
        return jsonify(result=res.result)
    else:
        return jsonify(result=res.result)
