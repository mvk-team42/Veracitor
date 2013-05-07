from flask import Flask, render_template, request, redirect, url_for, jsonify, abort

import json

from veracitor.web import app
from veracitor.web.utils import store_job_result
import veracitor.tasks.search as search
log = app.logger.debug

@app.route('/debug')
def debug():
    raise TypeError('Y U NO liek teh-bug?')

@app.route('/jobs/search/producers', methods=['GET','POST'])
def search_producers():
    """Performs a search in the database for producers that match the
    given parameters.

    URL Structure:
        /jobs/search/producers

    Method:
        POST

    Parameters:
        name (str): The name of a producer.
        type (str): The type of a producer.

    Returns:
        Upon success, returns an object with the job_id, ex:
        {"job_id": "baad-f00d-dead-beef-15"}

    Result when finished:
        An object with the producer data found.

    Errors:
        400 - Bad syntax/No name/type in request
        405 - Method not allowed

    """
    if not request.method == 'POST':
        abort(405)
    try:
        name = request.form['name']
        type_of = request.form['type']
        if type_of == '':
            type_of = None
    except:
        abort(400)
    res = search.get_producers.delay(name, type_of)
    store_job_result(res)
    return jsonify(job_id=res.id)

@app.route('/jobs/search/information', methods=['GET', 'POST'])
def search_information():
    """
    Performs a search in the database for information that matches the given
    parameters.
    
    """
    
    if not request.method == 'POST':
        abort(405)
    try:
        title_part = request.form['title_part']
        log(title_part)
        tags = request.form['tags']
        log(tags)
        
        try:
            startD = request.form['start_date']
            endD = request.form['end_date']
            res = search.get_information(title_part, tags,
                             startD=startD, endD=endD)
        except:
            res = seach.get_information(title_part, tags)

        store_job_result(res)
        return jsonify(job_id=res.id)
            
    except Exception as exp:
        log("Exception: "+str(type(exp)));
        abort(400)

    res = search.get_producers.delay(name, type_of)
    store_job_result(res)
    return jsonify(job_id=res.id)

    
    
