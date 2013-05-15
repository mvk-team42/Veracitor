# -*- coding: utf-8 -*-
"""
.. module:: user
    :synopsis: The user module contains the class needed to represent the user entity model. Class methods enable functionality related to the user entity.

.. moduleauthor:: Alfred Krappman <krappman@kth.se>
.. moduleauthor:: Fredrik Oeman <frdo@kth.se>
"""

from mongoengine import *
import group
import producer
import tag
import extractor
import datetime
import dbExceptions
import copy


class User(producer.Producer):
    """
    The User class inherhits from the Producer class 
    (which in turn inherhits from the mongoengine document class).
    Adds user-specific fields. Hard-codes the producer type_of field to
    'User'. Call save() to update database with the user
    (inserting it if it is not previously saved)
    or delete() to delete it from the database.

    The name field uniquely identifies a user in the database.
    """
    time_joined = DateTimeField()
    group_ratings = DictField()
    groups = ListField(ReferenceField('Group'))
    type_of = "User"
    password = StringField(required=True)
    pw_hash = StringField()
    email = StringField()
    
    def rate_group(self, name_of_group, rating):
        """
        Rate a group with specified rating. This will rate all the
        members of the group with rating. The user must own the group
        specified by (user_name, name_of_group).

        Args:
            name_of_group (str): The name of the group to be rated.
            
            rating (int): The rating to set on the group.

        Returns: True if a rating was succesfully set. False if the user
        did not own the group.
        
        Raises: TypeError if the arguments are of the wrong type.

        """
        if(type(name_of_group) is str and\
           type(rating) is int):
       
            if(not self.__user_owns_group(name_of_group)):
                return False
            self.group_ratings[name_of_group] = rating
            self.__rate_all_members(name_of_group, rating)
            return True

        else:
            raise TypeError("Problem with type of input variables.")
    
    

    def create_group(self, group_name, tag_name):
        """
        Creates a group with name specified by group_name
        and tag specified by tag_name. The group will be added
        to the user's group list and the new group's owner will 
        be set to this user. Note that this will save
        both the new group and the user to the database.

        Args:
            group_name (str): The name to give to the new group.
        
            tag_name (str): The tag to set on the new group.

        Returns:
            False if the user already owns a group with name
            equal to group_name. True if everything was succesfull.

        Raises:
            NotInDatabase if no tag with tag_name exists in the database.
        """        
        if(self.__user_owns_group(group_name)):
            return False
        try:
            tag = extractor.get_tag(tag_name)
        except dbExceptions.NotInDatabase:
            errMsg = "The tag specified does not exist"
            raise dbExceptions.NotInDatabase(errMsg)
        new_group = group.Group(name=group_name,
                                owner=self,
                                time_created=datetime.datetime.now(),
                                tag=tag)
        new_group.save()
        self.groups.append(new_group)
        self.save()
        return True
        
    
    def __rate_all_members(self, group_to_rate, rating):
        group_to_rate = extractor.get_group(self.name, group_to_rate)
        for producer_key,producer_obj in group_to_rate.producers.iteritems():
            self.rate_source(producer_obj, group_to_rate.tag, rating)
    
    def __user_owns_group(self, group_name):
        try:
            check_group = extractor.get_group(self.name, group_name)
        except dbExceptions.NotInDatabase:
            return None
        if(check_group.owner == self):
            return check_group
        else:
            return None
    
    def get_group_rating(self, req_group_name):
        """
        Get the rating this producer has set on the group
        with req_group_name.

        Args:
            req_group_name (str): The name of the group which the 
    
        Returns: The actual rating (an int). If the producer doesn't
        have a rating set on req_source, -1 will be returned.
    
        """
        return self.group_ratings[req_group_name]

    def add_to_group(self, req_group_name, producer_to_be_added):
        """
        Add a producer to specified group. This will also rate the producer
        with the tag set on group and the rating specified by the
        corresponding group rating.

        Args:
            req_group_name (str): The name of the group which 
            to add the producer to.

            producer_to_be_added (producer.Producer): The producer
            to add to the group.

        Returns: True if the producer was added and rated. 
        Otherwise False.

        """
        for group in self.groups:
            if group.name == req_group_name:
                group.producers[self.__safe_string(producer_to_be_added.name)]\
                                = producer_to_be_added
                group.save()
                self.rate_source(producer_to_be_added, 
                                 group.tag, 
                                 self.group_ratings[group.name])
                return True
                
        return False

    def remove_from_group(self, req_group_name, producer_to_be_deleted):
        """
        Removes a producer from the specified group.

        Args:
            req_group_name (str): The name of the group which 
            to remove the producer from.

            producer_to_be_deleted (producer.Producer): The producer
            to remove from the group.

        Returns: True if the producer was removed. 
        Otherwise False.

        """
        for group in self.groups:
            if group.name == req_group_name:
                try:
                    del group.producers[self.__safe_string(producer_to_be_deleted.name)]
                except KeyError:
                    return False
                return True
        return False

    def __safe_string(self, url):
        return url.replace(".", "|")
    
    
def testing():
    p2 = extractor.get_producer("Prod2")
    u1 = extractor.get_user("alfred")
    print u1.add_to_group("group1", p2)
    u1.rate_group("group1", 10)
    print u1.group_ratings
    print u1.source_ratings
    for p in u1.groups[0].producers.keys():
        print p
    
    
    
