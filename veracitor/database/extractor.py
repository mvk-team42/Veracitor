from mongoengine import *
import tag
import producer
import user
import information
import group
import re
import datetime
from dbExceptions import *

connect('mydb')

def get_producer(requested_name):
    extr_producer = producer.Producer.objects(name=requested_name)
    checkIfEmpty(extr_producer)
    return extr_producer[0]
    
def get_user(requested_name):
    extr_user = user.User.objects(name=requested_name)
    checkIfEmpty(extr_user)
    return extr_user[0]
    
def get_information(requested_title):
    extr_information = information.Information.objects(title=requested_title)
    checkIfEmpty(extr_information)
    return extr_information[0]
    
def get_group(owner_name, group_name):
    group = group.Group.objects(owner=owner_name, name=group_name)
    checkIfEmpty(group)
    return extr_group[0]
    
def get_tag(requested_name):
    extr_tag = tag.Tag.objects(name=requested_name)
    checkIfEmpty(extr_tag)
    return extr_tag[0]

def get_all_tags():
    return tag.Tag.objects()

def checkIfEmpty(extr_list):
    if (len(extr_list) == 0):
        raise NotInDatabase("Item not found")

def search_producers(possible_prod, type_of):
    """Returns a list of producers whose name includes possible_prod,
    and whose type_ exactly matches parameter type_.

    """
    #(?i) - case insensitive
    return producer.Producer.objects(name=re.compile('(?i)'+possible_prod), type_of=type_of)

def contains_producer(producer_name):
    p = producer.Producer.objects(name=producer_name)
    return len(p) != 0

def contains_user(user_name):
    u = user.User.objects(name=user_name)
    return len(u) != 0

def contains_information(info_title):
    i = information.Information.objects(title=info_title)
    return len(i) != 0

def contains_group(group_name):
    g = group.Group.objects(name=group_name)
    return len(g) != 0

def contains_tag(tag_name):
    t = tag.Tag.objects(name=tag_name)
    return len(t) != 0

def search_informations(possible_info, tags, startD, endD):
    """Returns a list of informations whose name includes possible_info,
    with at least one tag matching one of the provided tags,
    and whose date falls inbetween startD and endD


    """
    infos = information.Information.objects(title=re.compile('(?i)'+possible_info),
                                            time_published__lte=endD,
                                            time_published__gte=startD)
    to_be_ret = []
    for i in range (len(infos)):
        tmp_info_tags = infos[i].tags
        for j in range (len(tags)):
            if tags[j] in tmp_info_tags:
                to_be_ret.append(infos[i])
                break

    return to_be_ret
