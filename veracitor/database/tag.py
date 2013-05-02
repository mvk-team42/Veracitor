# -*- coding: utf-8 -*-
"""
.. module:: information
    :synopsis: The tag module contains the Tag class needed to represent the tag entity model.

.. moduleauthor:: Alfred Krappman <krappman@kth.se>
.. moduleauthor:: Fredrik Öman <frdo@kth.se> 
"""

from mongoengine import *


connect('mydb')


class Tag(Document):
    """
    The Tag class inherits from the mongoengine
    Document class. It defines fields needed to represent the tag 
    entity model. Call save() to update database with the tag
    (inserting it if it is not previously saved).
    or delete() to delete it from the database.
    
    The name field uniquely identifies a producer in the database.
    However, it also contains a field with alternate names for the tag.
    """
    
    name = StringField(required=True, unique=True)
    description = StringField()
    parent = ListField(ReferenceField('self'))
    valid_strings = ListField(StringField())

    #!!! not sure what this is supposed to be used for !!!
    def __eq__(self, other):
        """
        Compares an instance of the Tag class with another Tag instance.
        """
        if type(other) is type(self):
            return self.name == other.name
        else:
            return False
