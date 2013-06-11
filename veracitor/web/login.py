### This is a dirty hack to fix a temporary login/register.
### It's really insecure and shouldn't really be used at all.

"""
.. module:: login
    :synopsis: Implements login/register functions for the web client.

.. moduleauthor:: Anton Erholt <aerholt@kth.se>

"""

from flask import session, redirect, render_template, request, url_for, abort, jsonify
#from werkzeug.security import generate_password_hash, check_password_hash
from veracitor.web import app
from veracitor.web.utils import store_job_result
from veracitor.tasks import login

from veracitor.database import *
log = app.logger.debug


@app.route("/login", methods=["GET","POST"])
def login_user():
    """Logs the user in if needed.
    """

    if "user_name" in session:
        return redirect(url_for('index'))

    error = None
    user = None
    if session.get('error') != None:
        session.pop('error', None)


    if request.method == "POST":
        if not request.form['username']:
            error = "No username defined."
        elif not request.form['password']:
            error = "No password given."
        else:
            try:
                user = extractor.get_user(request.form['username'])
            except:
                print "Can't extract user from db."
                pass

        if not user:
            error = "No user with that username."
        elif not user.password == request.form['password']:
            error = "Wrong password."

        if error:
            session['error'] = error
        else:
            session['user_name'] = user.name

    return redirect(url_for("index"))



@app.route("/logout")
def logout():
    session.pop("user_name", None)
    session.pop("error", None)
    session.pop("crawls", None)
    return redirect(url_for("index"))



@app.route("/register", methods=['POST', 'GET'])
def register_user():
    """Registers a new user.

    URL Structure:
        ``/register``

    Method:
        POST

    Parameters:
        username (str): The username to be registered.
        password (str): The password to be used with the username to login.
    Returns:
        Upon success, returns an object with the job_id, ex::

        {"job_id": "ff92-23ad-232a-2334s-23"}

    Result when finished:
        *user_created (boolean)* : [True | False]
        *error (str)* : A string containing the error if any.

    Errors:
       * **405** -- Method not allowed

    """
    if request.method != 'POST':
        abort(405)
    res = login.register.delay(request.form.get('username'), request.form.get('password'))
    store_job_result(res)
    return jsonify(job_id=res.id)
