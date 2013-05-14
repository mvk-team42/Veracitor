# -*- coding: utf-8 -*-
"""
.. module:: producer
    :synopsis: The producer module contains classes needed to represent the producer entity model.

.. moduleauthor:: Alfred Krappman <krappman@kth.se>
.. moduleauthor:: Fredrik Oeman <frdo@kth.se>
"""

from mongoengine import *
import networkModel
import tag
import extractor
from dbExceptions import *
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
    info_ratings = DictField()
    type_of = StringField(required=True)
    # To allow the User class to inherhit.
    meta = {'allow_inheritance':'On'}

    def rate_source(self, source_to_rate, considered_tag, rating):
        """
        Use this method to make the producer rate a source considering
        a tag. Performs type checking.

        Args:
            source_to_rate (producer.Producer): The source which
            the producer should rate.
            
            considered_tag (tag.Tag): The tag which the rating is set under. 
        
            rating (int): The actual rating.

        Raises:
            TypeError: If any of the arguments are of the wrong type.
        
        """
        if(isinstance(source_to_rate, Producer) and\
           type(considered_tag) is tag.Tag and\
           type(rating) is int):
            # Has the producer rated the source previously?
            try:
                self.source_ratings[(source_to_rate.name)]\
                                   [considered_tag.name] = rating
            # If not, the key needs to be created.
            except KeyError:
                self.source_ratings[(source_to_rate.name)]\
                                    = {}
                self.source_ratings[(source_to_rate.name)]\
                                   [considered_tag.name] = rating
            self.save()
        else:
            raise TypeError("Problem with type of input variables.")

    def rate_information(self, information_to_rate, rating):
        """
        Use this method to make the producer rate an information object.

        Args:
            information_to_rate (information.Information): The information
            to be rated.
        
            rating (int): The actual rating.

        Raises:
            TypeError: If any of the arguments are of the wrong type.
        
        """

        # Should check type of information_to_rate but circular dependencies 
        if(\
           type(rating) is int):
            self.info_ratings[(information_to_rate.url)] = rating
        else:
            raise TypeError("Problem with type of input variables.")

    def get_all_source_ratings(self):
        return self.source_ratings

    def get_all_info_ratings(self):
        return self.info_ratings

    def get_source_rating(self, req_source, tag):
        """
        Get the rating this producer has set on req_source
        under tag.

        Args:
            req_source (producer.Producer): The source which the
            rating is set on.
            tag (tag.Tag): The tag the rating is set under.
    
        Returns: The actual rating (an int). If the producer doesn't
        have a rating set on req_source, -1 will be returned.
    
        """
        try:
            return self.source_ratings[req_source.name][tag.name]
        except KeyError:
            return -1

    def get_info_rating(self, req_info):
        """
        Get the rating this producer has set on req_info.

        Args:
            req_info (information.Information): The information which
            the rating is set on.
                
        Returns: The actual rating (an int). If the producer doesn't
        have a rating set on req_info, -1 will be returned.
    
        """
        try:
            return self.info_ratings[req_info.url]
        except KeyError:
            return -1

    def save(self):
        """
        Overrides save() inherhited from Document.
        Figures out whether to update the networkModel
        or to insert the saved producer into the networkModel.
        Calls check_rating_consistencies to remove dangling ratings.
        Follows this with the regular save() call in Document.
        

        Raises:
            NetworkModelException: If there is no global network created
            (and therefore no network to insert or update the saved producer
            into).

        """
        
        # Ensure that no ratings exist on deleted entities.
        self.check_rating_consistencies()
        
        if networkModel.graph is None:
            raise NetworkModelException("There is no Global Network created!")
        if(len(Producer.objects(name=self.name)) == 0):
            networkModel.notify_producer_was_added(self)
        else:
            networkModel.notify_producer_was_updated(self)

        self.prepare_ratings_for_saving()
        super(Producer, self).save()
        self.prepare_ratings_for_using()

    def prepare_ratings_for_saving(self):
        """
        Replaces "." in the keys of source_ratings and info_ratings with
        "|", to allow for saving in the database.
        Should only be called internally.
        """
        for rating in self.source_ratings.keys():
            self.source_ratings[self.__safe_string(rating)] = self.source_ratings.pop(rating)
        for rating in self.info_ratings.keys():
            self.info_ratings[self.__safe_string(rating)] = self.info_ratings.pop(rating)

    def prepare_ratings_for_using(self):
        """
        Replaces "|" in the keys of source_ratings and info_ratings with ".".
        Performs the opposite of prepare_ratings_for_saving to allow
        for normal usage.
        Should only be called internally.
        """
        for rating in self.source_ratings.keys():
            self.source_ratings[self.__unsafe_string(rating)] = self.source_ratings.pop(rating)
        for rating in self.info_ratings.keys():
            self.info_ratings[self.__unsafe_string(rating)] = self.info_ratings.pop(rating)

    def check_info_rating_consistency(self):
        """
        Removes dangling info_ratings.
        Achieves this by trying to extract the informations
        specified in the keys of info_ratings and possibly
        provoking a NotInDatabase (-exception).
        """
        info_ratings_to_be_deleted = []
        for k,v in self.info_ratings.items():
            try: 
                extractor.get_information(k)
            except NotInDatabase:
                info_ratings_to_be_deleted.append(k)
        for info in info_ratings_to_be_deleted:
            del self.info_ratings[info]

    def check_source_rating_consistency(self):
        """
        Removes dangling source_ratings.
        Achieves this by trying to extract the producers
        specified in the keys of source_ratings and possibly
        provoking a NotInDatabase (-exception).
        """
        source_ratings_to_be_deleted = []
        for source in self.source_ratings.keys():
            try:
                Producer.objects(name=source)[0]
            except IndexError:
                source_ratings_to_be_deleted.append(source)
        for source in source_ratings_to_be_deleted:
            del self.source_ratings[source]

    def check_rating_consistencies(self):
        """
        Combines check_info_rating_consistency with
        check_source_rating_consistency.
        """
        self.check_info_rating_consistency()
        self.check_source_rating_consistency()
                

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


    def add_information(self, info_to_add):
        """
        Adds an information to the infos-list.
        The info_to_add's publisher field is set
        to this producer.
    
        Returns: True if the information was added
        to the infos-list and the information's publisher
        is set to this producer, False otherwise.
        """
        for info in self.infos:
            if info == info_to_add:
                return False
        self.infos.append(info_to_add)
        for publisher in info_to_add.publishers:
            if publisher == self:
                return True
        info_to_add.publishers.append(self)
        return True

    def delete_information(self, info_to_del):
        """
        Reverts all actions of add_information.
        Deletes an information from the producer's infos_list
        and removes this producer from the information's publisher list.
        
        Returns: True if the information is removed from the producer's
        infos-list and 
        """
        found = False
        for x in range(len(self.infos)):
            if self.infos[x] == info_to_del:
                del self.infos[x]
                found = True
                break
        for x in range(len(info_to_del.publishers)):
            if info_to_del.publishers[x] == self:
                del info_to_del.publishers[x]
                if found:
                    return True
        return False



    def __safe_string(self, url):
        return url.replace(".", "|")
    def __unsafe_string(self, _str):
        return _str.replace("|", ".")
