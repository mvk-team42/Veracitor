from mongoengine import *


connect('mydb')


class Tag(Document):
    """Provides public fields
    mirroring underlying database object.
    Call save() to update database,
    delete() to delete object from database.
    
    """
    
    name = StringField(required=True)
    description = StringField()
    parent = ListField(ReferenceField('self'))
    valid_strings = ListField(StringField())

    def __eq__(self, other):
        if type(other) is type(self):
            return self.name == other.name
        else:
            return False
