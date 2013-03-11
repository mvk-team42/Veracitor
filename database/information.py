from mongoengine import *
import tag


class Information(Document):
    """Provides public fields mirroring
    underlying database object.
    Call save() to update database
    or delete() to delete object from the database.
    
    """
    name = StringField(required=True)
    description = StringField(required=True)
    url = StringField(required=True)
    time_published = DateTimeField(required=True)
    tags = ListField(ReferenceField(tag.Tag), required=True)
    publishers = ListField(ReferenceField('Producer', required=True))
    references = ListField(ReferenceField('self'))
    
