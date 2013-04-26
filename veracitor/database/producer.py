"""
.. module:: producer
    :synopsis: The producer module contains classes needed to represent
    the producer entity model.
"""

from mongoengine import *  
import globalNetwork
from dbExceptions import GlobalNetworkException
connect('mydb')

class SourceRating(EmbeddedDocument):
    """
    The SourceRating class inherits from the mongoengine
    EmbeddedDocument class. Is only meant to be used as a field value
    inside the Producer class. Defines fields describing a rating made 
    by one producer (the owner of a specific instance) on another producer
    (specified by the source field).
       
    """
    rating = IntField(required=True)
    tag = ReferenceField('Tag', required=True)
    source = ReferenceField('Producer', required=True)
    
class InformationRating(EmbeddedDocument):
    """
    The InformationRating class inherits from the mongoengine
    EmbeddedDocument class. Is only meant to be used as a field value
    inside the Producer class. Defines fields describing a rating made 
    by one producer (the owner of a specific instance) on an information
    (specified by the information field).
       
    """
    information = ReferenceField('Information', required=True)
    rating = IntField(required=True)
    
class Producer(Document):
    """
    The Producer class inherits from the mongoengince Document class.
    It defines needed to represent to producer entity model.
    Call save() to update database with the producer
    (inserting it if it is not previously saved).
    or delete() to delete object from the database.
    The name field uniquely identifies a producer in the database.

    """
    name = StringField(required=True, unique=True)
    first_name = StringField();
    last_name = StringField();
    description = StringField()
    url = StringField()
    infos = ListField(ReferenceField('Information'))
    source_ratings = ListField(EmbeddedDocumentField(SourceRating))
    info_ratings = ListField(EmbeddedDocumentField(InformationRating))
    type_of = StringField(required=True)
    # To allow the User class to inherhit from this.
    meta = {'allow_inheritance':'On'}
    
    def save(self):
        """
        Overrides save() inherhited from Document. 
        Figures out whether to update the globalNetwork
        or to insert the saved producer into the globalNetwork.
        Follows this with the regular save() call in Document. 
        
        Raises:
            GlobalNetworkException: If there is no global network created
            (and therefore no network to insert or update the saved producer
            into).

        """
        if globalNetwork.graph is None:
            raise GlobalNetworkException("There is no Global Network created!")
        if(len(Producer.objects(name=self.name)) == 0):
            globalNetwork.notify_producer_was_added(self)
        else:
            globalNetwork.notify_producer_was_updated(self)
        
        super(Producer, self).save()

    def delete(self):
        """
        Overrides delete() inherhited from Document.
        Begins with trying to delete the producer from the globalNetwork.
        Is idempotent, meaning that it can be called multiple times without
        damage done. If the producer isn't present in the globalNetwork
        or the database nothing is changed.

        Raises:

            GlobalNetworkException: If there is no global network created
            (and therefore no network to delete the producer from).
        
        """
        if globalNetwork.graph is None:
            raise GlobalNetworkException("There is no Global Network created!")
        if(len(Producer.objects(name=self.name)) == 0):
            return
        else:
            globalNetwork.notify_producer_was_removed(self)
            
        super(Producer, self).delete()

if __name__ == "__main__":
    globalNetwork.build_network_from_db()
    newP = Producer(name="ABC", type_of="MediaNetwork")
    newP.save()
    print globalNetwork.getDictionaryGraph()
    newP.delete()
