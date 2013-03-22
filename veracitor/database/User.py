from mongoengine import *
from Producer import Producer

connect('FOISERVER') # ej korrekt

class GroupRatings(EmbeddedDocument):
    """ Defines a object structure used by
    User to store user specific group rating 
    
    """
    group = ReferenceField(Document)
    rating = IntField(required=True)

class User(Producer):
    """Provides public fields mirroring
    underlying database object.
    Call save() to update database
    or delete() to delete object from the database.
    
    """
    password = StringField(required=True)
    time_joined = StringField(required=True) #Time eller date joined?
    group_ratings = ListField(EmbeddedDocumentField(GroupRatings))
    groups = ListField(ReferenceField(Document))
    

    
    
