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
import datetime
from dbExceptions import AlreadyExists

class GroupRating(EmbeddedDocument):
    """ Defines a object structure used by
    User to store user specific group rating.
    
    """
    group = ReferenceField('Group', required=True)
    rating = IntField(required=True)

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
    group_ratings = ListField(EmbeddedDocumentField(GroupRating))
    groups = ListField(ReferenceField('Group'))
    type_of = "User"
    password = StringField(required=True)
    pw_hash = StringField()
    email = StringField()

    def rate_group(self, group_to_rate, considered_tag, rating):
        found = False
        if(not self.__user_owns_group(group_to_rate.name)):
            return False
        for g_rating in self.group_ratings:
            if(g_rating.group == group_to_rate):
                g_rating.rating = rating
        if(not found):
            new_rating = GroupRating(group=group_to_rate,
                                     rating=rating)
            self.group_ratings.append(new_rating)
        self.__rate_all_members(group_to_rate, considered_tag, rating)
        return True

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
        for p in group_to_rate.producers:
            self.rate_source(p, considered_tag, rating)
    
    def __user_owns_group(self, group_name):
        for g in self.groups:
            if(g.name == group_name):
                return True
        return False
    
    def get_group_rating(self, req_group):
        for g_rating in self.group_ratings:
            if(g_rating.group == req_group):
                return g_rating.rating
        return -1
    
    

    
    
if __name__ == "__main__":
    u1 = User(name="hurse", password="hursefood")
    p1 = Producer(name="fax", type_of="mule")
    g1 = Group()
    g1.producers.add(p1)
    
    
    
