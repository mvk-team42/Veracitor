from mongoengine import *

connect('mydb')
__all__ = ["networkModel", "producer", "extractor", "group",
           "information", "user", "tag", "dbExceptions"]
