# -*- coding: utf-8 -*-
"""
.. module:: user
    :synopsis: The user module contains classes needed to represent the user entity model.

.. moduleauthor:: Alfred Krappman <krappman@kth.se>
.. moduleauthor:: Fredrik Öman <frdo@kth.se>
"""

from mongoengine import *
import producer
import group
import tag
import extractor
import datetime
import dbExceptions
import copy


class User(producer.Producer):
    """
    The Producer class inherits from the mongoengince Document class.
    It defines needed to represent to producer entity model.
    Call save() to update database with the producer
    (inserting it if it is not previously saved).
    or delete() to delete object from the database.
    The name field uniquely identifies a producer in the database.
    
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
        return self.group_ratings[req_group_name]

    def add_to_group(self, req_group_name, producer_to_be_added):
        
        for group in self.groups:
            if group.name == req_group_name:
                group.producers[self.__safe_string(producer_to_be_added.name)]\
                                = producer_to_be_added
                group.save()
                return True
                
        return False

    def remove_from_group(self, req_group_name, producer_to_be_deleted):
        for group in self.groups:
            if group.name == req_group_name:
                try:
                    del group.producers[self.__safe_string(producer_to_be_deleted.name)]
                except KeyError:
                    return False
                return True
        return False
        
    

    
    
def testing():
    p2 = extractor.get_producer("Prod2")
    u1 = extractor.get_user("alfred")
    print u1.add_to_group("group1", p2)
    u1.rate_group("group1", 10)
    print u1.group_ratings
    print u1.source_ratings
    for p in u1.groups[0].producers.keys():
        print p
    
    
    
