from networkx import to_dict_of_dicts, DiGraph
from tag import *
from producer import *
from information import *
from group import *
from user import *
from mongoengine import *

connect('mydb')

graph = None

def build_network_from_db():
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
            graph.add_edges_from([(p2.name, s.source.name)], {s.tag.name: s.rating})
    
    print to_dict_of_dicts(graph)

def getDictionaryGraph():
    return to_dict_of_dicts(graph)

def notify_producer_was_added(producer):
    print producer.name
    graph.add_node(producer.name)
    for s in producer.source_ratings:
        graph.add_edges_from([(producer.name, s.source.name)], {s.tag.name: s.rating})
    

def notify_information_was_added(information):
    graph.add_node(information.id)
    # add edges corr. to trust-relations


def notify_producer_was_removed(producer):
    graph.remove_node(producer.id)
    # edges are removed automatically :)

def notify_information_was_removed(information):
    graph.remove_node(information.id)
    # edges are removed automatically :)

def notify_producer_was_updated(producer):
    pass
    # add/remove edges corr. to trust-relations

def notify_information_was_updated(information):
    pass
    # add/remove edges corr. to trust-relations
    

"""Returns a list of tuples on the form (info rating rating A,
info rating rating B), where both A and B are ratings on the same
information but A is made by producer1 and B by producer2. Re-
turned ratings need to have been set under at least one of the
specified tags. Returns an empty list if no common ratings are
found."""    
def get_common_info_ratings(producer1, producer2, tags):
    return []
    
    
    
"""Returns a list of info ratings who are set at a level matching the
top/bottom 20% of the specified producer (I.E. ratings that
are unusually extreme relative to specified producer's ratings).
Returned ratings need to have been set under at least one of
specified tags."""
def get_extreme_info_ratings(producer, tags):
    return []
    
    
    
"""Returns an int equal to the difference between the two most differ-
ing ratings between producer1 and producer2."""
def get_max_rating_difference(producer1, producer2, tags):
    return 0

if __name__ == "__main__":
    build_network_from_db()
