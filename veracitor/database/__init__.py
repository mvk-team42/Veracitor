from mongoengine import *

connect('mydb')
__all__ = ["networkModel", "producer", "extractor", "group",
           "information", "user", "tag", "dbExceptions"]

import user
import information
user.User.register_delete_rule(group.Group, 'owner', CASCADE)
information.Information.register_delete_rule(producer.Producer, 'infos', PULL)
information.Information.register_delete_rule(information.Information, 'references', PULL)
