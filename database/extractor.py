from mongoengine import *
#from Tag import Tag
#from Tag import TagValidStrings
import tag
import producer
import user
import information
import group
import re
import datetime

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
    extr_tag = tag.Tag.objects(name=requested_name)
    return extr_tag[0]

def get_all_tags():
    return tag.Tag.objects()

def search_producers(possible_prod, type_):
    """Returns a list of producers whose name includes possible_prod,
    and whose type_ exactly matches parameter type_.

    """
    return producer.Producer.objects(name=re.compile('(?i)'+possible_prod), type_=type_)

def search_informations(possible_info, tags, startD, endD):
    """Returns a list of informations whose name includes possible_info,
    with at least one tag matching one of the provided tags,
    and whose date falls inbetween startD and endD

    """
    infos = information.Information.objects(name=re.compile('(?i)'+possible_info),
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


""" TESTING
print search_producers("g", "User")

date1 = datetime.datetime(year=1970,
                          month=12,
                          day=24)

date2 = datetime.datetime(year=2040,
                          month=12,
                          day=24)


tag1 = tag.Tag(name="Gardening", description="Hurrr HURRRRRR")
tag2 = tag.Tag(name="Cooking", description="Hurrr HURRRRRR")
print search_informations("dn", [tag1, tag2], date1, date2)
"""
