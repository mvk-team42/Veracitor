from mongoengine import *
#from Tag import Tag
#from Tag import TagValidStrings
import tag
import producer
import user
import information
import group

connect('mydb')

def get_producer(requested_name):
    extr_producer = producer.Producer.objects(name=requested_name)
    return extr_producer[0]
    
def get_user(requested_name):
    extr_user = user.User.objects(name=requested_name)
    return extr_user[0]
    
def get_information(requested_name):
    extr_information = information.Information.objects(name=requested_name)
    return extr_information[0]
    
def get_group(owner_name, group_name):
    group = group.Group.objects(owner=owner_name, name=group_name)
    return extr_group[0]
    
def get_tag(requested_name):
    extr_tag = tag.Tag.objects(_name=requested_name)
    return extr_tag[0]

