from mongoengine import *  
#from globalnetwork import *
import globalNetwork
from dbExceptions import GlobalNetworkException
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
    
    def save(self):
        if globalNetwork.graph is None:
            raise GlobalNetworkException("There is no Global Network created!")
        if(len(Producer.objects(name=self.name)) == 0):
            globalNetwork.notify_producer_was_added(self)
        else:
            globalNetwork.notify_producer_was_updated(self)
        
        super(Producer,self).save()


if __name__ == "__main__":
    globalNetwork.build_network_from_db()
    newP = Producer(name="ABC", type_of="MediaNetwork")
    newP.save()
    print globalNetwork.getDictionaryGraph()
    newP.delete()
