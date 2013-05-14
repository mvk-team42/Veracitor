from mongoengine import *

connect('mydb')

# What should be imported when importing everything from the database package.
__all__ = ["networkModel", "producer", "extractor", "group",
           "information", "user", "tag", "dbExceptions"]

import user
import information

# --- Deletion triggers ---

# When deleting a user its groups should also be deleted.
user.User.register_delete_rule(group.Group, 'owner', CASCADE)

# When deleting an information, it should also be removed from its publisher's
# information list.
information.Information.register_delete_rule(producer.Producer, 'infos', PULL)

# When deleting an information, references made to it by other informations
# should also be removed.
information.Information.register_delete_rule(information.Information, 'references', PULL)
