# -*- coding: utf-8 -*-
"""
.. module:: information
    :synopsis: The information module contains the Information class needed to represent the information entity model.

.. moduleauthor:: Alfred Krappman <krappman@kth.se>
.. moduleauthor:: Fredrik Öman <frdo@kth.se> 
"""

from mongoengine import *
import producer
import tag


class Information(Document):
    """
    The Information class inherits from the mongoengine Document class.
    It defines fields needed to represent the information entity model.
    Call save() to update database with the information
    inserting it if it is not previously saved).
    or delete() to delete it from the database.
    
    The url uniquely identifies an information in the database.
    """
    title = StringField(required=True)
    summary = StringField()
    url = StringField(required=True, unique=True)
    time_published = DateTimeField()
    tags = ListField(ReferenceField(tag.Tag))
    publishers = ListField(ReferenceField('Producer'))
    references = ListField(ReferenceField('self'))
    

Information.register_delete_rule(producer.Producer, 'infos', PULL)
