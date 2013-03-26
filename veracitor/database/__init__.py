from mongoengine import *

connect('mydb')
__all__ = ["globalNetwork", "information", "extractor", "group",
           "producer", "user", "tag"]
