from networkx import to_dict_of_dicts, DiGraph
from tag import *
from producer import *
from information import *
from group import *
from user import *
from mongoengine import *
import math
from numpy import array
connect('mydb')

graph = None

def get_global_network():
    global graph
    if graph is None:
        graph = build_network_from_db()
    return graph


def build_network_from_db():
    """Creates a new graph with data inserted from the database,
    overwrites the current graph. Only inserts producers into the 
    database as of now.

    """

    global graph
    # Users not included in graph
    producers = producer.Producer.objects(type_of__ne="User")
    graph = DiGraph()
   
    # Add all producers in the database as nodes
    for p1 in producers:
        graph.add_node(p1.name)
    
    # Add all producers' source ratings to the database as edges
    for p2 in producers:
        for s in p2.source_ratings:
            #graph.add_edges_from([(p2.name, s.source.name)], {s.tag.name: s.rating})
            graph.add_edge(p2.name, s.source.name, {s.tag.name: s.rating})
    
    return graph

def get_dictionary_graph():
    """Returns a python dictionary representation of the graph.

    """
    return to_dict_of_dicts(graph)

def notify_producer_was_added(producer):
    """Adds a new producer into the graph,
    connects it with existing producers.

    """
    graph.add_node(producer.name)
    for s in producer.source_ratings:
        #graph.add_edges_from([(producer.name, s.source.name)], {s.tag.name: s.rating})
        graph.add_edge(producer.name, s.source.name, {s.tag.name: s.rating})

def notify_producer_was_removed(producer):
    try:
        graph.remove_node(producer.name)
    except Exception:
        pass
    # edges are removed automatically :)


def notify_producer_was_updated(producer):
    notify_producer_was_removed(producer)
    notify_producer_was_added(producer)
    # add/remove edges corr. to trust-relations

def get_common_info_ratings(producer1, producer2, tags):
    """Returns a list of tuples on the form (info rating rating A,
    info rating rating B), where both A and B are ratings on the same
    information but A is made by producer1 and B by producer2. Re-
    turned ratings need to have been set under at least one of the
    specified tags. Returns an empty list if no common ratings are
    found.
    
    """    
    p1_info_ratings = producer1.info_ratings
    p2_info_ratings = producer2.info_ratings
    
    common_info_ratings = []
    #Optimize this..
    for info_1 in p1_info_ratings:
        for info_2 in p2_info_ratings:
            if info_1.information.title == info_2.information.title:
                if contains_common_tags(info_1.information.tags, tags):
                    common_info_ratings.append((info_1, info_2,))
                    
   
    return common_info_ratings

    
def contains_common_tags(tags_1, tags_2):
    for tag in tags_1:
        if tag in tags_2:
            return True

    return False


def get_extreme_info_ratings(producer, tags):
    """Returns a list of info ratings who differ from the mean by
    one standard deviation of the specified producer (I.E. ratings that
    are unusually extreme relative to specified producer's ratings).
    Returned ratings need to have been set under at least one of
    specified tags.

    """
    relevant_info_ratings = []
    relevant_info_ratings_ints = []
    total_sum = 0.0
    for info in producer.info_ratings:
        for tag in info.information.tags:
            if tag in tags:
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
    
    

def get_max_rating_difference(producer1, producer2, tags):
    """Returns an int equal to the difference between the two most differ-
    ing ratings between producer1 and producer2.
    If no common info_ratings were found -1 will be returned
    
    """
    common_info_ratings = get_common_info_ratings(producer1, producer2,tags)
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

"""
def notify_information_was_removed(information):

def notify_information_was_updated(information):
    pass
    # add/remove edges corr. to trust-relations
    
def notify_information_was_removed(information):
    graph.remove_node(information.id)
    # edges are removed automatically :)


"""
