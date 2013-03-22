from mongoengine import *

connect('mydb')
__all__ = ["information", "extractor", "group",
           "producer", "user", "tag"]
