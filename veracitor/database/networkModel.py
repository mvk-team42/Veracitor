# -*- coding: utf-8 -*-
"""
.. module:: networkModel
    :synopsis: The purpose of the global network is to ease the accessing of the database through building a NetworkX DiGraph. Defines a set of convenience functions performing tasks related to traversing the data in the database.


The purpose of the global network is to ease the accessing of the database through building a NetworkX DiGraph. Defines a set of convenience functions performing tasks related to traversing the data in the database.

The nodes of the graph correspond to a producer and consist of 
their unique (string) name. The edges correspond to the
source_ratings they have defined on each other, with attributes
on each edge specifying the actual rating and under which
tag.name the rating was set.

.. moduleauthor:: Alfred Krappman <krappman@kth.se>
.. moduleauthor:: Fredrik Öman <frdo@kth.se> 
"""

from networkx import to_dict_of_dicts, DiGraph
from tag import *
from producer import *
from information import *
from group import *
from user import *
from mongoengine import *
import extractor
import math
from numpy import array
connect('mydb')

graph = None

def get_global_network():
    """
    Returns a graph containing all the producers currently in 
    the database with their ratings set on each other.
    Creates it if it is not already created.
    If the graph is not already built a call to this 
    function will result in a new graph being constructed
    by calling build_network_from_db().

    Returns: the global network (a NetworkX DiGraph)

    """
    global graph
    if graph is None:
        # Create a new graph.
        graph = build_network_from_db()
    return graph


def build_network_from_db():
    """
    Creates a new graph with data inserted from the database,
    overwrites the current graph. This function will extract all
    producers from the database and iterate through their source_ratings
    to build the global network. Therefore, the time to complete running this
    function depends on the number of producers in the database
    and the number of ratings they have set on each other.

    Returns: the global network (a NetworkX DiGraph)

    """

    global graph
    # Users not included in graph.
    producers = producer.Producer.objects(type_of__ne="User")
    graph = DiGraph()
   
    # Add all producers in the database as nodes.
    for p1 in producers:
        graph.add_node(p1.name)
    
    # Add all producers' source ratings to the database as edges,
    # where the actual rating and corresponding tag is set as an
    # edge attribute.
    for p2 in producers:
        for s in p2.source_ratings:
            graph.add_edge(p2.name, s.source.name, {s.tag.name: s.rating})
    
    return graph

def get_dictionary_graph():
    """
    Returns a dictionary representation of the graph using
    the NetworkX to_dict_of_dicts() function.

    The dictionary would be structured as follows if
    producer1 has rated producer2, but producer2 hasn't
    rated anyone.

    {
        producer1.name: 
            {producer1.source_rating1.source.name: 
                {producer1.source_rating1.tag.name: 
                 producer1.source_rating1.rating}
            }
        producer2.name: 
            { }
    }

    """
    return to_dict_of_dicts(graph)

def notify_producer_was_added(producer):
    """
    Adds a new producer into the graph,
    connects it with existing producers.
    This should not be called by anything other than
    the producer.Producer object on a .save() call.
    Ignore this function if that confuses you. 

    Args:
        producer (producer.Producer): The producer object
        to be inserted into the networkModel.
    """
    graph.add_node(producer.name)
    for s in producer.source_ratings:
        graph.add_edge(producer.name, s.source.name, {s.tag.name: s.rating})

def notify_producer_was_removed(producer):
    """
    Deletes a producer from the graph,
    removes outgoing and incoming edges.
    This should not be called by anything other than
    the producer.Producer object on a .delete() call.
    Ignore this function if that confuses you.
    
    Args:
        producer (producer.Producer): The producer object
        to be deleted from the networkModel.
    
    """
    try:
        # edges are removed automatically :)
        graph.remove_node(producer.name)
    except Exception:
        # Removing nonexistant node is allowed.
        pass
    


def notify_producer_was_updated(producer):
    """
    Updates the graph with the given producer.
    This should not be called by anything other than
    the producer.Producer object on a .save() call.
    Ignore this function if that confuses you.
    
    Args:
        producer (producer.Producer): The producer object
        to be updated in the networkModel.

    """
    # Possibly cheap/slow implementation.
    notify_producer_was_removed(producer)
    notify_producer_was_added(producer)

def get_overall_difference(producer_name1, producer_name2, tag_names):
    """Returns the average difference in ratings 
    made by producer_name1 and producer_name2
    on the same informations. 
    Informations need to contain at least one tag in tag_names.
    If no common_info_ratings exists -1 will be returned.

    Args:
        producer_name1 (str): The first producer to consider.
        
        producer_name2 (str): The second producer to consider.

        tag_names ([str]): The tags specifying which ratings to consider.

    Returns:
        A float that is the average value of the difference in rating. 
        If they have no info ratings in common -1.0 will be returned.

    """
    common_info_ratings = get_common_info_ratings(producer_name1, 
                                                  producer_name2, tag_names)
    # No info ratings in common?
    if len(common_info_ratings) == 0:
        return -1.0
    sum_diff_ratings = 0
    for info_rating_t in common_info_ratings:
        # Increment sum with the difference in opinion 
        # of the currently selected info-rating-tuple
        sum_diff_ratings += math.fabs(info_rating_t[0].rating - info_rating_t[1].rating)
    avg = sum_diff_ratings/len(common_info_ratings)

    return avg

def get_common_info_ratings(producer_name1, producer_name2, tag_names):
    """
    Returns a list of tuples on the form (info rating rating A,
    info rating rating B), where both A and B are ratings on the same
    information but A is made by producer1 and B by producer2. Re-
    turned ratings need to have been set under at least one of the
    specified tags. Returns an empty list if no common ratings are
    found.

    Args:
        producer_name1 (str): The first producer to consider.
        
        producer_name2 (str): The second producer to consider.

        tag_names ([str]): The tags specifying which informations to consider.
    
    Returns:
        Let's say producer 1 has rated dn-ledare with info_rating1.
                  producer 2 has rated dn-ledare with her own info_rating2.
        They have both rated with the same tag specified.
        The return value will be (info_rating1, info_rating2,).
    
    """    
    p1_info_ratings = extractor.get_producer(producer_name1).info_ratings
    p2_info_ratings = extractor.get_producer(producer_name2).info_ratings
    
    common_info_ratings = []
    # Candidate for later optimization.
    for info_1 in p1_info_ratings:
        for info_2 in p2_info_ratings:
            # Are these ratings set on the same information?
            if info_1.information.title == info_2.information.title:
                # Does the information have a tag matching requested tags?
                if __contains_common_tags(info_1.information.tags, tag_names):
                    # The ratings are set on the same information and conforms to tags.
                    # Therefore considered as a common info rating.
                    common_info_ratings.append((info_1, info_2,))
                    
   
    return common_info_ratings

    
def __contains_common_tags(tags_1, tag2_names):
    for tag in tags_1:
        if tag.name in tag2_names:
            return True

    return False


def get_extreme_info_ratings(producer_name, tag_names):
    """Returns a list of info ratings who differ from the mean by
    one standard deviation of the specified producer (I.E. ratings that
    are unusually extreme relative to specified producer's ratings).
    Returned ratings need to have been set under at least one of
    specified tags.

    Args:
        producer_name (str): The producer to consider.

        tag_names ([str]): The tags specifying which informations to consider.

    Returns: 
        [producer.InformationRating]. Ignoring tags, let's say a producer
        has made the ratings 4, 6, 5, 1 and 10. This function would calculate
        the mean of these (I.E. 5) and the standard deviation of these
        (2.925747...) and return those info_ratings with a rating that
        deviates from the mean by the standard deviation. In this
        case the info_ratings with the ratings 1 and 10 would be returned
        in a list.
    """
    producer = extractor.get_producer(producer_name)
    
    # Will contain info ratings set on informations
    relevant_info_ratings = []
    relevant_info_ratings_ints = []
    total_sum = 0.0
    for info in producer.info_ratings:
        for tag in info.information.tags:
            if tag.name in tag_names:
                relevant_info_ratings.append(info)
                relevant_info_ratings_ints.append(info.rating)
                total_sum += info.rating
                break
    
    mean = (total_sum)/len(relevant_info_ratings)

    extremes = []
    np_array = array(relevant_info_ratings_ints)
    std = np_array.std()
    for info in relevant_info_ratings:
        diff = math.fabs(info.rating - mean)
        if diff > std:
            extremes.append(info)
    return extremes
    
    

def get_max_rating_difference(producer_name1, producer_name2, tag_names):
    """
    Returns an int equal to the difference between the two most differ-
    ing ratings between producer1 and producer2.
    If no common info_ratings were found -1 will be returned.

    Args:
        producer_name1 (str): The first producer to consider.
        
        producer_name2 (str): The second producer to consider.

        tag_names ([str]): The tags specifying which informations to consider.

    Returns:
        an int. Producer1 has made the ratings 2 on DNLedare and 4 on SvDLedare.
                Producer2 has made the ratings 2 on DNLedare and 1 on SvDLedare.
        They most differ in opinion on SvDLedare, and the returned int will then
        be 4-1 = 3. SvDLedare need to have at a tag that is also in tag_names.
    
    """
    producer1 = extractor.get_producer(producer_name1)
    producer2 = extractor.get_producer(producer_name2)

    common_info_ratings = get_common_info_ratings(producer_name1, producer_name2,tag_names)
    if len(common_info_ratings) == 0:
        return -1 

    max_diff = 0
    for common_tuple in common_info_ratings:
       diff = math.fabs(common_tuple[0].rating - common_tuple[1].rating)
       if diff > max_diff:
           max_diff = diff

    return max_diff

if __name__ == "__main__":
    build_network_from_db()

