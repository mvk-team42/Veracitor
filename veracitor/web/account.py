
"""
.. module:: account.py
    :synopsis: Implements some simple user handling functions

.. moduleauthor:: Anton Erholt <aerholt@kth.se>

"""

from flask import session, redirect, render_template, request, url_for, abort, jsonify
#from werkzeug.security import generate_password_hash, check_password_hash
from veracitor.web import app

from veracitor.database import *
log = app.logger.debug


@app.route("/user/delete", methods=["POST", "GET"])
def delete_user():
    """Deletes the user from the database.
    Requires you to be authenticated as an admin.

    URL Structure:
        ``/user/delete``

    Method:
        POST

    Parameters:
        user_name (str): The username of the user to be removed.
    Returns:
        An object with a boolean if the user was removed or not.

    Errors:
       * **405** -- Method not allowed
       * **401** -- Unauthorized if the logged in user is not admin.
       * **404** -- No such username.

    """

    if not request.method == 'POST':
        abort(405)
    if not str(session.get('user_name')) == 'admin':
        abort(401)

    try:
        username = request.form.get('user_name')
        nm=networkModel.build_network_from_db() # TODO , move this to task?
        user = extractor.get_user(username)
        user.delete()
    except:
        abort(404)

    return jsonify(result=username)
