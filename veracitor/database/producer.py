# -*- coding: utf-8 -*-
"""
.. module:: producer
    :synopsis: The producer module contains classes needed to represent the producer entity model.

.. moduleauthor:: Alfred Krappman <krappman@kth.se>
.. moduleauthor:: Fredrik Öman <frdo@kth.se> 
"""

from mongoengine import *  
import networkModel
import tag
import information
from dbExceptions import NetworkModelException
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
    
    #TODO implement. Should overwrite earlier ratings on same tag/source
    def rate_source(self, source_to_rate, considered_tag, rating):
        found = False
        for s_rating in self.source_ratings:
            if(s_rating.source == source_to_rate and\
               s_rating.tag == considered_tag):
                s_rating.rating = rating
                found = True
        if(not found):
            new_rating = SourceRating(source=source_to_rate, 
                                      tag=considered_tag, 
                                      rating=rating)
            self.source_ratings.append(new_rating)
        

    def rate_information(self, info_to_rate, rating):
        found = False
        for i_rating in self.info_ratings:
            if(i_rating.information == info_to_rate):
                i_rating.rating = rating
                found = True
        if(not found):
            new_rating = InformationRating(information=info_to_rate,
                                           rating=rating)
            self.info_ratings.append(new_rating)
    

    def get_source_rating(self, req_source, req_tag):
        for s_rating in self.source_ratings:
           if(s_rating.source == req_source and s_rating.tag == req_tag):
                return s_rating.rating
        return -1 
            
    def get_info_rating(self, req_info):
        for i_rating in self.info_ratings:
            if(i_rating.information == req_info):
                return i_rating.rating
        return -1
    
    def save(self):
        """
        Overrides save() inherhited from Document. 
        Figures out whether to update the networkModel
        or to insert the saved producer into the networkModel.
        Follows this with the regular save() call in Document. 
        
        Raises:
            NetworkModelException: If there is no global network created
            (and therefore no network to insert or update the saved producer
            into).

        """
        if networkModel.graph is None:
            raise NetworkModelException("There is no Global Network created!")
        if(len(Producer.objects(name=self.name)) == 0):
            networkModel.notify_producer_was_added(self)
        else:
            networkModel.notify_producer_was_updated(self)
        
        super(Producer, self).save()

    def delete(self):
        """
        Overrides delete() inherhited from Document.
        Begins with trying to delete the producer from the networkModel.
        Is idempotent, meaning that it can be called multiple times without
        damage done. If the producer isn't present in the networkModel
        or the database nothing is changed.

        Raises:

            NetworkModelException: If there is no global network created
            (and therefore no network to delete the producer from).
        
        """
        if networkModel.graph is None:
            raise NetworkModelException("There is no Global Network created!")
        if(len(Producer.objects(name=self.name)) == 0):
            return
        else:
            networkModel.notify_producer_was_removed(self)
            
        super(Producer, self).delete()

if __name__ == "__main__":
    p1 = Producer(name="fax", type_of="mule")
    p2 = Producer(name="fux", type_of="donkey")
    t1 = tag.Tag(name="gardening")
    p1.rate_source(p2, t1, 5)
    p1.rate_source(p2, t1, 4)
    #p1.rate_source(p2, "hgurur", 1)
    print p1.source_ratings
    print p1.get_source_rating(p2, t1)
    print information.Information
    i1 = information.Information(name="korre", url="seaweed.com")
    p1.rate_information(i1, 2)
    print p1.get_source_rating(p2, t1)
    print p1.get_info_rating(i1)
    
