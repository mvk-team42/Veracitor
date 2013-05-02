# -*- coding: utf-8 -*-

# ratings.py
# ========

"""
.. module:: ratings
    :synopsis: Defines server logic for the ratings tab

.. moduleauthor:: Martin Runelöv <mrunelov@kth.se>
.. moduleauthor:: Daniel Molin <dmol@kth.se>

"""


from flask import Flask, render_template, request, redirect, url_for, jsonify

import json

from flask import render_template
from veracitor.web import app
from veracitor.web.utils import store_job_result
from veracitor.database import user, group, information, extractor

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
        Upon success, returns the user as a json object.

    Errors:
        400 - Bad syntax/No name/type in request
        405 - Method not allowed

    """
    if not request.method == 'POST':
        return "nope"
        abort(405)
    try:
        user_id = request.form['user_id']
        userObj = extractor.get_user(user_id)

        source_ratings = [{'name' : s.source.name,
                           'tag' : s.tag.name,
                           'rating': s.rating }
                          for s in userObj.source_ratings]

        info_ratings = [{'title':ir.information.title,
                                'rating':ir.rating} for ir in userObj.info_ratings]

        groups = [{'name' : g.name,
                   'description' : g.description,
                   'owner' : g.owner,
                   'producers' : [p.name for p in g.producers]}
                  for g in userObj.groups]

        userDict = {'name' : userObj.name,
                    'description' : userObj.description,
                    'type_of' : userObj.type_of,
                    'source_ratings' : source_ratings,
                    'groups' : groups,
                    'group_ratings' : [{'group':gr.group, 'rating':gr.rating} for gr in userObj.group_ratings],
                    'info_ratings' : info_ratings}

    except NotInDatabase:
        return "not in databaseteafw"
    except:
        return "bajs"
        abort(400)

    return jsonify(user=userDict)

@app.route('/jobs/ratings/rate_producer', methods=['GET', 'POST'])
def rate_producer():
    if not request.method == 'POST':
        abort(405)
    try:
        user = extractor.get_user(request.form['username']) # TODO: Use real session user
        user.rate_source(request.form['producer'], request.form['tag'], int(request.form['rating']))
        #user.save()
    except:
        abort(400)

    # TODO: Render json

@app.route('/jobs/ratings/rate_information', methods=['GET', 'POST'])
def rate_information():
    if not request.method == 'POST':
        abort(405)
    try:
        user = extractor.get_user(request.form['username']) # TODO: Use real session user
        user.rate_information(request.form['information'], int(request.form['rating']))
        #user.save()
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
        user = extractor.get_user(request.form['username']) # TODO: Use real session user
        user.create_group(request.form['name'])
        #user.save()
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
        user = extractor.get_user(request.form['username']) # TODO: Use real session user
        user.rate_group(request.form['name'], request.form['tag'],
                        int(request.form['rating']))
        #user.save()
    except:
        abort(400)

    # TODO: Render json

@app.route('/ratings')
def ratings():
    """
    Initializes the ratings tab

    """
    user_data = get_user()

    return render_template('ratings_tab.html', vera=user_data)
