from flask import Flask, render_template, request, redirect, url_for, jsonify

import json

from veracitor.web import app
from veracitor.web.utils import store_job_result
import veracitor.tasks.ratings as ratings

@app.route('/jobs/ratings/user', methods=['GET', 'POST'])
def get_user():
    """Gets the specified user from the database.

    URL Structure:
        /jobs/ratings/user

    Method:
        POST

    Parameters:
        name (str): The name of the user.

    Returns:
        Upon success, returns an object with the job_id, ex:
        {"job_id": "ff92-23ad-232a-2334s-23"}
        {"job_id": "baad-f00d-dead-beefs-15"}

    Result when finished:
        An object with the user data found.

    Errors:
        400 - Bad syntax/No name/type in request
        405 - Method not allowed

    """

    if not request.method == 'POST':
        abort(405)
    try:
        user_id = request.form['user_id']
    except:
        abort(400)
    res = ratings.get_user.delay(user_id)
    store_job_result(res)
    return jsonify(job_id=res.id)


@app.route('/jobs/ratings/information_objects', methods=['GET', 'POST'])
def get_information_objects():
    """Gets the specified user from the database.

    URL Structure:
        /jobs/ratings/user

    Method:
        POST

    Parameters:
        name (str): The name of the user.

    Returns:
        Upon success, returns an object with the job_id, ex:
        {"job_id": "ff92-23ad-232a-2334s-23"}
        {"job_id": "baad-f00d-dead-beefs-15"}

    Result when finished:
        An object with the user data found.

    Errors:
        400 - Bad syntax/No name/type in request
        405 - Method not allowed

    """

    if not request.method == 'POST':
        abort(405)
    try:
        tag = request.form['tag']
    except:
        abort(400)
    res = ratings.get_information_objects.delay(user_id)
    store_job_result(res)
    return jsonify(job_id=res.id)


@app.route('/jobs/ratings/information_object', methods=['GET', 'POST'])
def get_information_object():
    """Gets the specified user from the database.

    URL Structure:
        /jobs/ratings/user

    Method:
        POST

    Parameters:
        name (str): The name of the user.

    Returns:
        Upon success, returns an object with the job_id, ex:
        {"job_id": "ff92-23ad-232a-2334s-23"}
        {"job_id": "baad-f00d-dead-beefs-15"}

    Result when finished:
        An object with the user data found.

    Errors:
        400 - Bad syntax/No name/type in request
        405 - Method not allowed

    """

    if not request.method == 'POST':
        abort(405)
    try:
        possible_info = request.form['search_string']
        tag = request.form['tag']
    except:
        abort(400)
    res = ratings.get_information_object.delay(possible_info, tag)
    store_job_result(res)
    return jsonify(job_id=res.id)
