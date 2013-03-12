from mongoengine import *

connect('mydb')

class Group(Document):
    """Provides public fields mirroring
    underlying database object.
    Call save() to update database
    or delete() to delete object from the database.
    
    """
    name = StringField(required=True) 
    description = StringField()
    owner = ReferenceField((Document), required=True)
    tags = ListField(ReferenceField('Tag'), required=True)
    producers = ListField(ReferenceField('Producer'))
    time_created = DateTimeField(required=True)
    
    
    
    
