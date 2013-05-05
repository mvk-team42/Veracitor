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
    
    def rate_group(self, name_of_group, name_of_tag, rating):
        if(not self.__user__owns_group(name_of_group)
            return False;
        if(type(name_of_group) is str and\
           type(name_of_tag) is str and\
           type(rating) is int):
            self.group_ratings[name_of_group] = rating
            self.__rate_all_members(name_of_group, name_of_tag, rating)
            return True
        else:
            raise TypeError("Problem with type of input variables.")

    
    

    def create_group(self, group_name):
        if(self.__user_owns_group(group_name)):
            return False
        new_group = group.Group(name=group_name,
                                owner=self,
                                time_created=datetime.datetime.now())
        new_group.save()
        #self.groups.append(new_group)
        return True
        
    
    def __rate_all_members(self, group_to_rate, considered_tag, rating):
        group_to_rate = extractor.get_group(self, group_to_rate)
        considered_tag = extractor.get_tag(considered_tag)
        for p in group_to_rate.producers:
            self.rate_source(p, considered_tag, rating)
    
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
        return self.groups[req_group_name]
    
    

    
    
def testing():
    u1 = extractor.get_user("hurse")
    u1.save()
    p1 = extractor.get_producer("mrunelov")
    p1.save()
    u1.create_group("de_stable")
    u1.groups[0].append(p1)
    u1.rate_group("de_stable", "Trust", 5)
    
    
    
