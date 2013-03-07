from mongoengine import *

connect('pentagon lol') # :D

class Group(Document):
    """Provides public fields mirroring
    underlying database object.
    Call save() to update database
    or delete() to delete object from the database.
    
    """
    name = StringField(required=True)
    description = StringField(required=False)
    owner = ReferenceField((Document), required=True)
    tags = ListField(ReferenceField(Document), required=True)
    producers = ListField(ReferenceField(Document), required=True)
    time_created = IntField(required=True) # date?
    
    
    
    
