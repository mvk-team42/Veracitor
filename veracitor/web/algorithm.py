# -*- coding: utf-8 -*-
from flask import request, redirect, url_for, render_template, abort, jsonify,\
    make_response
from veracitor.web import app
from veracitor.web.utils import store_job_result

import veracitor.tasks.algorithms as algorithms

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
    if not request.method == 'POST':
        abort(405)
    try:
        source = request.form['source']
        sink = request.form['sink']
        tag = request.form['tag']
    except KeyError, AttributeError:
        abort(400)

    res = algorithms.sunny.delay(source, sink, tag)
    store_job_result(res)
    return jsonify(job_id=res.id)
