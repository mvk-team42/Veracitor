# -*- coding: utf-8 -*-
"""
.. module:: producer
    :synopsis: The producer module contains classes needed to represent the producer entity model.

.. moduleauthor:: Alfred Krappman <krappman@kth.se>
.. moduleauthor:: Fredrik Öman <frdo@kth.se> 
"""

from mongoengine import *  
import globalNetwork
import tag
import information
from dbExceptions import GlobalNetworkException
connect('mydb')

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
    first_name = StringField()
    last_name = StringField()
    description = StringField()
    url = StringField()
    infos = ListField(ReferenceField('Information'))
    source_ratings = DictField()
    #source_ratings = ListField(EmbeddedDocumentField(SourceRating))
    #info_ratings = ListField(EmbeddedDocumentField(InformationRating))
    info_ratings = DictField()
    type_of = StringField(required=True)
    # To allow the User class to inherhit from this.
    meta = {'allow_inheritance':'On'}
    
    #TODO implement. Should overwrite earlier ratings on same tag/source
    def rate_source(self, source_to_rate, considered_tag, rating):
        if(type(source_to_rate) is Producer and\
           type(considered_tag) is tag.Tag and\
           type(rating) is int):
            self.source_ratings[(source_to_rate, considered_tag,)] = rating
        else:
            raise TypeError("Problem with type of input variables.")

    def rate_information(self, information_to_rate, rating):
        if(type(information_to_rate) is information.Information and\
           type(rating) is int):
            self.info_ratings[information_to_rate] = rating
        else:
            raise TypeError("Problem with type of input variables.")

    def get_all_source_ratings(self):
        return self.source_ratings
    
    def get_all_info_ratings(self):
        return self.info_ratings
    
    def get_source_rating(self, req_source, tag):
        return self.source_ratings[(req_source, tag,)]

    def get_info_rating(self, req_info):
        return self.info_ratings[req_info]
    
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

# Demonstrates use of rating methods
if __name__ == "__main__":
    p1 = Producer(name="fax", type_of="mule")
    p2 = Producer(name="fux", type_of="donkey")
    t1 = tag.Tag(name="gardening")
    p1.rate_source(p2, t1, 5)
    #p1.rate_source(p2, "hgurur", 1)
    print p1.get_all_source_ratings()
    print information.Information
        
    i1 = information.Information(name="korre", url="seaweed.com")
    p1.rate_information(i1, 2)
    print p1.get_source_rating(p2, t1)
    print p1.get_info_rating(i1)
    

