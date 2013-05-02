# -*- coding: utf-8 -*-
"""
.. module:: group
    :synopsis: The group module contains the Group class needed to represent the group entity model.

.. moduleauthor:: Alfred Krappman <krappman@kth.se>
.. moduleauthor:: Fredrik Öman <frdo@kth.se> 
"""

from mongoengine import *

connect('mydb')

class Group(Document):
    """
    The Group class inherhits from the mongoenginde Document class.
    Group defines fields that defines a group containing producers and
    a user owner. Call save() to update database with the group or delete()
    to delete from the database.
    
    """
    name = StringField(required=True) 
    description = StringField()
    owner = ReferenceField(('User'), required=True)
    tags = ListField(ReferenceField('Tag'), required=True)
    producers = ListField(ReferenceField('Producer'))
    time_created = DateTimeField(required=True)
    
    
    
    
