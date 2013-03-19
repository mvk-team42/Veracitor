from mongoengine import *
import producer

connect('FOISERVER') # ej korrekt

class GroupRating(EmbeddedDocument):
    """ Defines a object structure used by
    User to store user specific group rating 
    
    """
    group = ReferenceField('Group', required=True)
    rating = IntField(required=True)

class User(producer.Producer):
    """Provides public fields mirroring
    underlying database object.
    Call save() to update database
    or delete() to delete object from the database.
    
    """
    password = StringField(required=True)
    time_joined = DateTimeField() #Time eller date joined?
    group_ratings = ListField(EmbeddedDocumentField(GroupRating))
    groups = ListField(ReferenceField('Group'))
    type_ = "User"
    

    
    