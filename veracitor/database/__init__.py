from mongoengine import *

connect('mydb')
__all__ = ["networkModel", "information", "extractor", "group",
           "producer", "user", "tag"]
