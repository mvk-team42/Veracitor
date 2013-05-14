# -*- coding: utf-8 -*-
"""
.. module:: group
    :synopsis: The group module contains the Group class needed to represent the group entity model.

.. moduleauthor:: Alfred Krappman <krappman@kth.se>
.. moduleauthor:: Fredrik Öman <frdo@kth.se> 
"""

from mongoengine import *
import networkModel
import datetime

import extractor

from dbExceptions import NotInDatabase
connect('mydb')

class Group(Document):
    """
    The Group class inherhits from the mongoenginde Document class.
    Group defines fields that defines a group containing producers and
    a user owner. Call save() to update database with the group or delete()
    to delete from the database. Note that, if save() is called for the
    first time the group will be automatically appended to the owner's
    group list, and a save() call is subsequently made on the owner.
    
    """
    name = StringField(required=True) 
    description = StringField()
    owner = ReferenceField('User', required=True)
    tag = ReferenceField('Tag', required=True)
    producers = DictField()
    time_created = DateTimeField(required=True)
    
    def save(self):
        """
        Overrides save() inherhited from Document.
        Only does something if this group isn't previously saved
        to the database. Appends self to owner's group list and
        calls save() on owner.
        
        """
        first_time = False
        try:
            extractor.get_group(self.owner.name, self.name)
        except NotInDatabase:
            first_time = True
        super(Group, self).save()
        if(first_time):
            self.owner.groups.append(self)
            self.owner.save()

    def delete(self):
        # Delete owner's group rating
        try:
            del self.owner.group_ratings[self.name]
        except KeyError:
            pass
            
        super(Group, self).delete()

def testing():
    networkModel.build_network_from_db()
    u1 = User(name="donkey", password="123")
    u1.save()
    u1.create_group("TestGroup4", "Trust")
    

