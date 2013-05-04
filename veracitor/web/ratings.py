# -*- coding: utf-8 -*-

# ratings.py
# ========

"""
.. module:: ratings
    :synopsis: Defines server logic for the ratings tab

.. moduleauthor:: Martin RunelÃ¶v <mrunelov@kth.se
.. moduleauthor:: Daniel Molin <dmol@kth.se>

"""

from flask import Flask, render_template, session, request, redirect, url_for, jsonify, abort

from veracitor.web import app
from veracitor.web.utils import store_job_result, get_user_as_dict
from veracitor.database import user, group, information, extractor

import veracitor.tasks.ratings as ratings

log = app.logger.debug


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
        Upon success, returns the user as a json object.

    Errors:
        400 - Bad syntax/No name/type in request
        405 - Method not allowed

    """
    if not request.method == 'POST':
        return "nope"
        abort(405)
    try:
        user_dict = get_user_as_dict(session['user_name'])
    except NotInDatabase:
        return "not in database"
    except:
        return "bla"
        abort(400)

    return jsonify(user=user_dict)

@app.route('/jobs/ratings/rate_producer', methods=['GET', 'POST'])
def rate_producer():
    if not request.method == 'POST':
        abort(405)
    try:
        user = extractor.get_user(session['user_name'])
        user.rate_source(request.form['producer'],
                         request.form['tag'], int(request.form['rating']))
    except:
        abort(400)

    # TODO: Render json

@app.route('/jobs/ratings/rate_information', methods=['GET', 'POST'])
def rate_information():
    if not request.method == 'POST':
        abort(405)
    try:
        user = extractor.get_user(session['user_name'])
        user.rate_information(request.form['information'],
                              int(request.form['rating']))
    except:
        abort(400)

    # TODO: Render json

@app.route('/jobs/ratings/create_group', methods=['GET', 'POST'])
def create_group():
    """
    Creates a group with the specified name.

    """
    if not request.method == 'POST':
        abort(405)
    try:
        user = extractor.get_user(session['user_name'])
        user.create_group(request.form['name'])

        return request.form['name']
    except:
        abort(400)

    # TODO: Render json

@app.route('/jobs/ratings/rate_group', methods=['GET', 'POST'])
def rate_group():
    """
    Rate a group.

    """
    if not request.method == 'POST':
        abort(405)
    try:
        user = extractor.get_user(session['user_name'])

        if len(user.groups[request.form['name']].producers) > 0:
            user.rate_group(request.form['name'], request.form['tag'],
                            int(request.form['rating']))
        else:
            abort(400)
    except Exception, e:
        log(e)
        abort(400)

    # TODO: Render json


@app.route('/jobs/ratings/get_used_tags', methods=['GET', 'POST'])
def get_used_tags():
    """
    Returns a list of all tags that the user has rated producers with.

    """
    if not request.method == 'POST':
        abort(405)
    try:
        user = extractor.get_user(session['user_name'])
                
        tags_used = list(set([sr.tag.name for sr in user.source_ratings]))

        return jsonify(tags=tags_used)
    except:
        abort(400)
