from mongoengine import * 


connect('mydb')

class SourceRating(EmbeddedDocument):
    """Defines public fields used by
       Producer to store source ratings
       together with a tag.
       
    """
    rating = IntField(required=True)
    tag = ReferenceField('Tag', required=True)
    source = ReferenceField('Producer', required=True)
    
class InformationRating(EmbeddedDocument):
    """Defines public fields used by
       Producer to store information ratings.
       
    """
    information = ReferenceField('Information', required=True)
    rating = IntField(required=True)

class Producer(Document):
    """Provides public fields mirroring
    underlying database object.
    Call save() to update database
    or delete() to delete object from the database.
    
    """
    name = StringField(required=True, unique=True)
    description = StringField()
    url = StringField()
    infos = ListField(ReferenceField('Information'))
    source_ratings = ListField(EmbeddedDocumentField(SourceRating))
    info_ratings = ListField(EmbeddedDocumentField(InformationRating))
    type_of = StringField(required=True)
    meta = {'allow_inheritance':'On'}
    


