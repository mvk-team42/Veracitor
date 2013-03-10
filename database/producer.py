from mongoengine import * 

connect('mydb')

class SourceRating(EmbeddedDocument):
    """Defines public fields used by
       Producer to store source ratings
       together with a tag.
       
    """
    rating = IntField(required=True)
    tag = ReferenceField(Document, required=True)
    source = ReferenceField(Document, required=True)
    
class InformationRating(EmbeddedDocument):
    """Defines public fields used by
       Producer to store information ratings.
       
    """
    information = ReferenceField(Document, required=True)
    rating = IntField(required=True)

class Producer(Document):
    """Provides public fields mirroring
    underlying database object.
    Call save() to update database
    or delete() to delete object from the database.
    
    """
    name = StringField(required=True)
    description = StringField(required=True)
    url = StringField(required=True)
    infos = ListField(ReferenceField(Document))
    source_ratings = ListField(EmbeddedDocumentField(SourceRating))
    info_ratings = ListField(EmbeddedDocumentField(InformationRating))
    type_ = StringField(required=True)
    meta = {'allow_inheritance':'On'}
    


