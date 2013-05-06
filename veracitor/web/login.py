### This is a dirty hack to fix a temporary login.
### It's really insecure and shouldn't really be used at all.

from flask import session, redirect, render_template, request, url_for
#from werkzeug.security import generate_password_hash, check_password_hash
from veracitor.web import app

from veracitor.database import *


@app.route("/login", methods=["GET","POST"])
def login():
    """
    
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
    return redirect(url_for("index"))
    


@app.route("/register")
def register():
    pass