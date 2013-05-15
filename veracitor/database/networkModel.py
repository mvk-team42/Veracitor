# -*- coding: utf-8 -*-
"""
.. module:: networkModel
   :synopsis: The purpose of the network model is to ease the accessing of the database through building a NetworkX DiGraph. .
   
The nodes of the graph correspond to a producer and consist of their
unique (string) name. The edges correspond to the  source_ratings they
have defined on each other, with attributes on each edge specifying
the actual rating and under which tag.name the rating was set.

.. moduleauthor:: Alfred Krappman <krappman@kth.se>
.. moduleauthor:: Fredrik Oeman <frdo@kth.se> 
"""

from networkx import to_dict_of_dicts, DiGraph
from tag import *
from producer import *
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

    Returns: the global network (type NetworkX DiGraph)

    """

    global graph
    # Users not included in graph.
    producers = Producer.objects()
    graph = DiGraph()
   
    # Add all producers in the database as nodes.
    for p1 in producers:
        p1.prepare_ratings_for_using()
        graph.add_node(p1.name)
    
    # Add all producers' source ratings to the database as edges,
    # where the actual rating and corresponding tag is set as an
    # edge attribute.
    for p2 in producers:
        p2.prepare_ratings_for_using()
        for k,v in p2.source_ratings.iteritems():
            graph.add_edge(p2.name, k, v)
    
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
    Adds a new producer to the graph,
    connects it with existing producers.
    This should not be called by anything other than
    the producer.Producer object on a .save() call.
    Ignore this function if that confuses you. 

    Args:
        producer (producer.Producer): The producer object
        to be inserted into the networkModel.
    """
    graph.add_node(producer.name) #Add the producer (just the name) to the graph
    for k,v in producer.source_ratings.iteritems(): #For all source ratings
            graph.add_edge(producer.name, k, v) #Edge to the rated producer

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
        # Edges are removed automatically :)
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
    #Get all outgoing edges from this producer in the network graph.
    out_edges = graph.out_edges(nbunch=[producer.name], data=True)
    tmp_edges = []
    for k,v in producer.source_ratings.iteritems(): #For each source rating
        try:
            graph.remove_edge(producer.name, k) #Remove possibly the old edge
        except Exception: 
            pass #Ignore any raised exception
        graph.add_edge(producer.name, k, v) #Add the possibly updated edge
        tmp_edges.append((producer.name,k,v))

    #For each edge before the update
    for edge in out_edges: 
        #If the old edge didn't exist in the updated producer node
        if edge not in tmp_edges:
            #Remove the edge from the graph
            graph.remove_edge(edge[0], edge[1])


def get_overall_difference(producer_name1, producer_name2, tag_names):
    """
    Returns the average difference in ratings 
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
    #Get all common information ratings under a common tag.
    common_info_ratings = get_common_info_ratings(producer_name1, 
                                                  producer_name2, tag_names)
    # No info ratings in common?
    if len(common_info_ratings) == 0:
        return -1.0

    sum_diff_ratings = 0
    for info_rating_t in common_info_ratings:
        # Increment sum with the difference in opinion 
        # of the currently selected info-rating-tuple
        sum_diff_ratings += math.fabs(info_rating_t[0] - info_rating_t[1])
    
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
    tmp_string = ""
    val = 0;
    #For each information rated by producer 1
    for k, v in p1_info_ratings.iteritems():
        try:
            val = p2_info_ratings[k] #Get the rating for the same information 
                                     #rated by producer 2.
            #If the information has been given one or more tags specified in
            #tag_names.
            if __contains_common_tags(extractor.get_information(tmp_string).tags,
                                      tag_names):
                #Create and append a tuple with the ratings given by producer 1
                #and producer 2.
                common_info_ratings.append( (v, val) )

        except Exception: #If producer 2 had no such information rating            
            pass          #ignore the raised exception.
    
    return common_info_ratings
    
def __contains_common_tags(tags_1, tag2_names):
    for tag in tags_1:
        if tag.name in tag2_names:
            return True

    return False


def get_extreme_info_ratings(producer_name, tag_names):
    """Returns a dictionary mapping information titles
    with ratings set on them who differ from the mean by
    one standard deviation of the specified producer (I.E. ratings that
    are unusually extreme relative to specified producer's ratings).
    Returned ratings need to have been set under at least one of
    specified tags.

    Args:
        producer_name (str): The producer to consider.

        tag_names ([str]): The tags specifying which informations to consider.

    Returns: 
        {Information.title : rating_value }. Ignoring tags, let's say a producer
        has made the ratings 4, 6, 5, 1 and 10. This function would calculate
        the mean of these (I.E. 5) and the standard deviation of these
        (2.925747...) and return a dictionary
        mapping the title of Informations with a rating that
        deviates from the mean by the standard deviation. In this
        case the Information ratings with the ratings 1 and 10 would be returned
        in a dictionary.
    """
    producer = extractor.get_producer(producer_name)
    
    # Will contain info ratings set on informations
    relevant_info_ratings = {}
    relevant_info_ratings_ints = []
    total_sum = 0.0 #Value will be used to calculate the mean of info_ratings
    #For each information rated by the producer
    for k,v in producer.info_ratings.iteritems():
        #For each tag given to the current information object
        for tag in extractor.get_information(k.replace("|", ".")).tags:
            #If the name of the tag is specified in tag_names
            if tag.name in tag_names:
                relevant_info_ratings[k] = v #Store the information title and
                                             #and rating.
                relevant_info_ratings_ints.append(v) 
                total_sum += v
                break #Common tag found, proceed to the next information rating.
    
    
    if relevant_info_ratings_ints: #Found one or more information objects.
        #Calculate the mean of the information ratings found.
        mean = (total_sum)/len(relevant_info_ratings_ints)
    else: 
        return [] 

 
    
    
    std = _stddev(relevant_info_ratings_ints) #Calculate the standard deviation
    extremes = {}
    #For each information rating found
    for k,v in relevant_info_ratings.iteritems():
        diff = math.fabs(v - mean) #Absolute difference
        if diff > std: #If the difference exceeds one standard deviation
                       #then v will be considered as an extreme rating.
            extremes[k.replace("|", ".")] = v

    return extremes
    
def get_difference_on_extremes(p1, p2, tags):
    """
    Calcualates the diffence on extremes for two producers' info ratings
    (χ(n, n') in *Kuter, Golbeck 2010*).
    
    Quote from the paper:
    
    *A decision D(n, e) is considered extreme if it is more than one
    standard deviation from the mean rating assigned by n. χ(n,n') is
    computed as the average absolute difference on this set.*
    
    .. note::
        "Average absolute difference" is using the median of the extreme-sets
        as the central tendency, m(X). This is used most often according to 
       `Wikipedia <http://en.wikipedia.org/wiki/Absolute_deviation>`_.

    .. note::
       It's not obvious what set(s) Kuter and Golbeck are referring to when
       talking about the average absolute difference. Hopefully I made the 
       right decision when calculating the AAD for the combined set of 
       extreme ratings, that is AAD(p1_extremes UNION p2_extremes).

       *- Daniel Molin*

    Args:
       *p1, p2 (unicode)*: The input producers.
       
       *tags (list of unicodes)*: The list of tag names to consider when
       finding info ratings.

    Returns:
       χ(p1, p2) = average absolute difference of the extreme ratings by the
       input producers.

       *None* if no extremes could be found for one or
       both of the producers.

    """
    p1_extremes = set([x.rating for x in get_extreme_info_ratings(p1, tags)])
    p2_extremes = set([x.rating for x in get_extreme_info_ratings(p2, tags)])

    if len(p1_extremes) == 0 or len(p2_extremes) == 0:
        # No extremes to compare, return None
        return None

    extremes_combined = p1_extremes | p2_extremes
    extreme_median = median(list(extremes_combined))

    D = fsum([math.fabs(x-extreme_median) for x in extremes_combined])/ \
        len(extremes_combined)

    return D

def get_belief_coefficient(p1, p2, tags):
    """
    Calulates σ(n,n') from *Equation (1)* in *Kuter, Golbeck 2010*.

    """
    get_global_network()
    overall_difference = get_overall_difference(p1,p2,tags)
    thetas = [overall_difference]
    for n in graph.successors(p1):
        if n != p2:
            thetas.append(get_overall_difference(p1,n,tags))

    np_array = array(thetas)
    mean = np_array.mean()
    stddev = np_array.std()

    if overall_difference > (mean+stddev):
        coefficient = -1
    elif overall_difference < (mean - stddev):
        coefficient = 1
    else:
        # Pearson coefficient based on common info ratings.
        # It compares two datasets (the common decisions).
        # Maybe use 'from scipy.stats.stats import pearsonr'

        common_info_ratings = get_common_info_ratings(p1,p2,tags)
        n = len(common_info_ratings)
        if n > 1:
            sum_p1 = sum(
                [x.rating for (x,y) in common_info_ratings])
            sum_p2 = sum(
                [y.rating for (x,y) in common_info_ratings])
            sum_p1_p2 = sum(
                [x.rating*y.rating for (x,y) in common_info_ratings])
            sum_p1_squared = sum(
                [x.rating**2 for (x,y) in common_info_ratings])
            sum_p2_squared = sum(
                [y.rating**2 for (x,y) in common_info_ratings])
        
            coefficient = float((n*sum_p1_p2 - sum_p1*sum_p2))/ \
                float((math.sqrt((n*sum_p1_squared-((sum_p1)**2))*(n*sum_p2_squared - ((sum_p2)**2)))))
        else:
            coefficient = 0

    return coefficient


def _stddev(numbers):
    np_array = array(numbers)
    return np_array.std()

def _mean(numbers):
    np_array = array(numbers)
    return np_array.mean() 

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

    common_info_ratings = get_common_info_ratings(producer_name1, 
                                                  producer_name2,tag_names)
    #No common information ratings were found
    if len(common_info_ratings) == 0:
        return -1 

    max_diff = 0
    #For each (info_rating,info_rating)-tuple
    for common_tuple in common_info_ratings:
        #Calculate the absolute difference between the two ratings
        diff = math.fabs(common_tuple[0] - common_tuple[1])
        if diff > max_diff: #If the difference is greater than the largest
                            #difference found so far.
            max_diff = diff #Update the maximum difference

    return max_diff

