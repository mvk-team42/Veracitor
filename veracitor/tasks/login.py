# login.py
# ========
# Defines user register task

try:
    from veracitor.tasks.tasks import taskmgr
except:    
    from tasks import taskmgr

from database import *

@taskmgr.task
def register(username, password):

    error = None
    if not request.form['username']:
        error = "Please enter a username."
    elif not request.form['password']:
        error = "Please enter a password."
    elif not len(request.form['username']) > 3:
        error = "Please choose a longer username."
    elif not len(request.form['password']) > 3:
        error = "Please choose a longer password."
    else:
        username = request.form['username']
        password = request.form['password']

    user = extractor.get_user(username)
    if user != None:
        error = "Username already taken."

    if error != None:
        return {"error": error,
                "user_created": False}

    usr = user.User()
    usr.name = username
    usr.password = password
    usr.save()

    return {"user_created": True}

