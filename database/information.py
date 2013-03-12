from mongoengine import *
import tag


class Information(Document):
    """Provides public fields mirroring
    underlying database object.
    Call save() to update database
    or delete() to delete object from the database.
    
    """
    name = StringField(required=True, unique=True)
    description = StringField()
    url = StringField(required=True)
    time_published = DateTimeField()
    tags = ListField(ReferenceField(tag.Tag))
    publishers = ListField(ReferenceField('Producer'))
    references = ListField(ReferenceField('self'))
    
