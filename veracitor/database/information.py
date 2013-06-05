# -*- coding: utf-8 -*-
"""
.. module:: information
    :synopsis: The information module contains the Information class needed to represent the information entity model.

.. moduleauthor:: Alfred Krappman <krappman@kth.se>
.. moduleauthor:: Fredrik Oeman <frdo@kth.se> 
"""

from mongoengine import *
import producer
import tag
import extractor


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
    
    def __str__(self):
        _str = "##Information-Entity##\n"
        _str += self.__print_help("Title", self.title)
        _str += self.__print_help("URL", self.url)
        _str += self.__print_help("Summary", self.summary)
        _str += self.__print_help("Time published", self.time_published)
        
        _str += "Tags: "
        if(len(self.tags) == 0):
            _str += "None\n"
        else:
            _str += "\n"
            for tag in self.tags:
                _str += "               * " + tag.name + "\n"

        _str += "Publishers: "
        if(len(self.publishers) == 0):
            _str += "None\n"
        else:
            _str += "\n"
            for prod in self.publishers:
                _str += "               * " + prod.name + "\n"

        _str += "References: "
        if(len(self.references) == 0):
            _str += "None\n"
        else:
            _str += "\n"
            for ref in self.references:
                _str += "               * " + ref.url + "\n"

        _str += "##############\n"
        return _str
        
    def __print_help(self, attr_to_print, attr):
        _str = attr_to_print + ": "
        if(attr == None):
            _str += "not set\n"
        else:
            _str += attr + "\n"
        return _str
