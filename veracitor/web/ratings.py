# -*- coding: utf-8 -*-

# ratings.py
# ========

"""
.. module:: ratings
    :synopsis: Defines server logic for the ratings tab

.. moduleauthor:: Martin Runelöv <mrunelov@kth.se
.. moduleauthor:: Daniel Molin <dmol@kth.se>

"""

from flask import Flask, render_template, session, request, redirect, url_for, jsonify, abort

from veracitor.web import app, utils
from veracitor.web.utils import store_job_result, get_user_as_dict
from veracitor.database import user, group, information, extractor

import veracitor.tasks.ratings as ratings

log = app.logger.debug


@app.route('/jobs/ratings/render', methods=['GET', 'POST'])
def render_ratings():
    """
    Fetches the current user and renders the Ratings tab

    Method:
        POST
    
    Returns:
        *html* (str): The html used to render the Ratings tab
        *producers* (dict): A dictionary of the producers that the currently logged in user has rated
        *information* (dict): A dictionary of the information that the currently logged in user has rated

    Errors:
        400 - Bad syntax
        405 - Method not allowed
    
    """
    if not request.method == 'POST':
        abort(405)
    try:
        userDict = utils.get_user_as_dict(session['user_name'])
        producers = userDict['source_ratings']
        information = userDict['info_ratings']
        html = render_template('tabs/ratings_tab_content.html', user=userDict)
    except Exception, e:
        log(e)
        abort(400)

    return jsonify(html=html, producers=producers, information=information)

@app.route('/jobs/ratings/rate_producer', methods=['GET', 'POST'])
def rate_producer():
    """
    Rates a producer

    Method:
        POST

    Parameters:
        *producer* (str): The producer to be rated
        *tag* (str): The tag with which to rate
        *rating* (str): The rating with which to rate

    Errors:
        400 - Bad syntax
        405 - Method not allowed

    """
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
    """
    Rates information

    Method:
        POST

    Parameters:
        *information* (str): The information to be rated
        *rating* (str): The rating with which to rate

    Errors:
        400 - Bad syntax
        405 - Method not allowed

    """
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

    Method:
        POST

    Parameters:
        *name* (str): The name of the group that will be created

    Returns:
        The name of the created group
        
    Errors:
        400 - Bad syntax
        405 - Method not allowed

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
    Rates a group

    Method:
        POST

    Parameters:
        *name* (str): The name of the group to be rated
        *rating* (str): The rating with which to rate

    Errors:
        400 - Bad syntax
        405 - Method not allowed

    Returns:
        A status string (currently without purpose)

    """
    if not request.method == 'POST':
        abort(405)
    try:
        user = extractor.get_user(session['user_name'])
        
        if len(extractor.get_group(session['user_name'],request.form['name']).producers) > 0:
            user.rate_group(request.form['name'], request.form['rating'])
        else:
            abort(400)
        return "Success"
    except:
        return "Fail"
        abort(400)

    # TODO: Render json


@app.route('/jobs/ratings/get_used_prod_tags', methods=['GET', 'POST'])
def get_used_prod_tags():
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


@app.route('/jobs/ratings/get_used_info_tags', methods=['GET', 'POST'])
def get_used_info_tags():
    """
    Returns a list of all tags that the user has rated information with

    """
    if not request.method == 'POST':
        abort(405)
    try:
        # TODO: Try this! (nested list comprehension)
        user = extractor.get_user(session['user_name'])
        tags_used = list(set((tag.name for tag in ir.information.tags) for ir in user.info_ratings))

        return jsonify(tags=tags_used)
    except:
        abort(400)
