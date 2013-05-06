# login.py
# ========
# Defines user register task

try:
    from veracitor.tasks.tasks import taskmgr
except:    
    from tasks import taskmgr

from veracitor.database import *

@taskmgr.task
def register(username, password):

    error = None
    if not username:
        error = "Please enter a username."
    elif not password:
        error = "Please enter a password."
    elif not len(username) > 3:
        error = "Please choose a longer username."
    elif not len(password) > 3:
        error = "Please choose a longer password."
    else:
        usr = user.User.objects.filter(name=username)
        if len(usr) != 0:
            error = "Username already taken."

    if error != None:
        return {"error": error,
                "user_created": False}

    usr = user.User()
    usr.name = username
    usr.password = password
    usr.save()

    return {"user_created": True}

