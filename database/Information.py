from mongoengine import *
import Tag

class Information(Document):
    """Provides public fields mirroring
    underlying database object.
    Call save() to update database
    or delete() to delete object from the database.
    
    """
    name = StringField(required=True)
    description = StringField(required=True)
    url = StringField(required=True)
    time_published = StringField(required=True)
    tags = ListField(ReferenceField(Tag.Tag), required=True)
    publishers = ListField(ReferenceField(Document), required=True)
    references = ListField(ReferenceField('self'))
    
