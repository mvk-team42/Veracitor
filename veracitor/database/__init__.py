from mongoengine import *

connect('mydb')
__all__ = ["networkModel", "producer", "extractor", "group",
           "information", "user", "tag", "dbExceptions"]

import user
user.User.register_delete_rule(group.Group, 'owner', CASCADE)
