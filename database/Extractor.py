from mongoengine import *
from Tag import Tag
from Tag import TagValidStrings
import Producer
import User
import Information
import Group

connect('mydb')

def get_producer(requested_name):
    producer = Producer.objects(name=requested_name)
    return producer[0]
    
def get_user(requested_name):
    user = User.objects(name=requested_name)
    return user[0]
    
def get_information(requested_name):
    information = Information.objects(name=requested_name)
    return information[0]
    
def get_group(owner_name, group_name):
    group = Group.objects(owner=owner_name, name=group_name)
    return group[0]
    
def get_tag(requested_name):
    tag = Tag.objects(_name=requested_name)
    return Tag.objects()[0]

