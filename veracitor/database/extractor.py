# -*- coding: utf-8 -*-
"""
.. module:: extractor
     :synopsis: Specifies functionality to communicate with a database which uses MongoDB.

.. moduleauthor:: Alfred Krappman <krappman@kth.se>
.. moduleauthor:: Fredrik Öman <frdo@kth.se>
"""


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
    """
        Search for a producer specified by a given name.

        Args:
            requested_name (str): The name of the requested producer.
        Returns:
            The requested producer object.
        Raises:
            NotInDataBase: The producer couldn't be found in the database.

	"""
    extr_producer = producer.Producer.objects(name=requested_name)
    __checkIfEmpty(extr_producer)
    return extr_producer[0]


def producer_create_if_needed(requested_name, type_if_new):
	try:
		return get_producer(requested_name)
	except NotInDatabase:
		new_producer = producer.Producer(
		            name = requested_name,
		            type_of = type_if_new)
		new_producer.save()
		return new_producer

def get_user(requested_name):
    """
        Search for a user specified by a given name.

        Args:
            requested_name (str): The name of the requested user.

        Returns:
            The requested user object.

        Raises:
            NotInDataBase: The user couldn't be found in the database.

    """
    extr_user = user.User.objects(name=requested_name)
    __checkIfEmpty(extr_user)
    return extr_user[0]

def get_information(info_url):
    """
        Search for an information object specified by URL.

        Args:
            url (str): The URL of the requested information object.

        Returns:
            The requested information object.

        Raises:
            NotInDataBase: The information object couldn't be found
                           in the database.
    """
    extr_information = information.Information.objects(url=info_url)
    __checkIfEmpty(extr_information)
    return extr_information[0]

def get_group(owner_name, group_name):
    """
        Search for a group specified by an owner and a group name.

        Args:
            owner_name (str): The name of the owner of the requested group.
            group_name (str): The name of the requested group.

        Returns:
            The requested group object.

        Raises:
            NotInDataBase: If the owner does not exist or if no such group
                           could be found it the database.

    """
    extr_owner = get_user(owner_name)

    extr_group = group.Group.objects(owner=extr_owner, name=group_name)
  
    __checkIfEmpty(extr_group)

    return extr_group[0]

def get_tag(requested_name):
    """
        Search for a tag specified by a given name.

        Args:
            requested_name (str): The name of the requested tag.

        Returns:
            The requested tag object.

        Raises:
            :class:`veracitor.database.dbExceptions.NotInDatabase`: No such tag could be found in the database.

    """
    extr_tag = tag.Tag.objects(name=requested_name)
    __checkIfEmpty(extr_tag)
    return extr_tag[0]

def get_tag_create_if_needed(requested_name):
	try:
		return get_tag(requested_name)
	except NotInDatabase:
		new_tag = tag.Tag(
			name = requested_name,
			valid_strings = [requested_name]
			)
		new_tag.save()
		return new_tag

def get_all_tags():
    """
        Fetches all current tag object in the database.

        Returns:
            A list of all the current tag objects in the database.

    """
    return tag.Tag.objects()

def __checkIfEmpty(extr_list):
    """
        Used by all get methods to check if query resulted in a empty list and
        raises a exception if that was the case.

        Args:
            extr_list (list): The list to be checked.
        Raises:
            NotInDataBase: If the given list is empty.

    """
    if (len(extr_list) == 0):
        raise NotInDatabase("Item not found")

def search_producers(possible_prod, type_of):
    """
        Searches the database for producers whose name includes a specified
        name and whose type exactly matches a specified type.

        Args:
            possible_prod (str): A string that partly matches a name of a
                                 producer.
            type_of (str): The type of the requested producers.
        Returns:
            A list of zero or more producer objects.
    """
    #(?i) - case insensitive
    if type_of:
        return producer.Producer.objects(name=re.compile('(?i)'+possible_prod), type_of=type_of)
    else:
        return producer.Producer.objects(name=re.compile('(?i)'+possible_prod))

def contains_producer_with_name(producer_name):
    """
        Check if a producer specified by name exist in the database.

        Args:
            requested_name (str): The name of the producer.

        Returns:
            True if a match was found otherwise False.

    """
    p = producer.Producer.objects(name=producer_name)
    return len(p) != 0

def contains_producer_with_url(producer_url):
    """
        Check if a producer specified by a given url exist in the database.

        Args:
            producer_url (str): URL of the requested producer.

        Returns:
            True if a match was found otherwise False.
    """
    p = producer.Producer.objects(url=producer_url)
    return len(p) != 0

def contains_user(user_name):
    """
        Check if a user specified by name exist in the database.

        Args:
            requested_name (str): The name of the user.

        Returns:
            True if a match was found otherwise False.
    """
    u = user.User.objects(name=user_name)
    return len(u) != 0

def contains_information(info_url):
    """
        Check if an information object specified by URL exist
        in the database.

        Args:
            url (str): The URL of the information object.

        Returns:
            True if a match was found otherwise False.
    """
    i = information.Information.objects(url=info_url)
    return len(i) != 0

def contains_group(group_name):
    """
        Check if an information object specified by title exist
        the database.

        Args:
            info_title (str): The title of the information object.

        Returns:
            True if a match was found otherwise False.
    """
    g = group.Group.objects(name=group_name)
    return len(g) != 0

def contains_tag(tag_name):
    """
        Check if a tag specified by title exist the database.

        Args:
            info_title (str): The name of the requested tag.

        Returns:
            True if a match was found otherwise False.
    """
    t = tag.Tag.objects(name=tag_name)
    return len(t) != 0

def search_informations(possible_info, tags, startD, endD):
    """
        Searches the database for information objects whose name includes
        a specified name, with at least one tag matching one or more provided
        tags and whose date falls inbetween a specified time frame.

        Args:
            possible_info (str): A title which will partly match a title
                                 of a information object.
            tags ([tag.Tag]): A list of tag objects.
            startD (datetime.Date): Lower bound of the time frame.
            endD (datetime.Date): Upper bound of the time frame.

        Returns:
            A list of zero or more information objects.
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
