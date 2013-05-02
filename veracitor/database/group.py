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
import user
import extractor
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
    owner = ReferenceField(user.User, required=True)
    #tags = ListField(ReferenceField('Tag'), required=True)
    producers = ListField(ReferenceField('Producer'))
    time_created = DateTimeField(required=True)
    
    def save(self):
        first_time = False
        if(not extractor.contains_group(self.name)):
            first_time = True
        super(Group, self).save()
        if(first_time):
            self.owner.groups.append(self)
            self.owner.save()

if __name__ == "__main__":
    networkModel.build_network_from_db()
    u1 = user.User(name="hurseeee", password="123")
    u1.save()
    g1 = Group(name="kdjdkj", owner=u1, time_created=datetime.datetime.now())
    g1.save()
    print u1.groups[0].name
