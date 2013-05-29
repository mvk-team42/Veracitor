# -*- coding: utf-8 -*-

""" 
.. module:: tidaltrust
    :synopsis: The TidalTrust algorithm as specified by Jennifer Golbeck (2007), with some extended functionality.

.. moduleauthor:: Daniel Molin <dmol@kth.se>
.. moduleauthor:: Martin Runelov <mrunelov@kth.se>
"""

import sys
import networkx as nx
from copy import deepcopy
from itertools import chain

def tidal_trust(source, sink, graph, tag):
    """ 
    Calculates a trust value between the source and the sink nodes 
    in the given NetworkX DiGraph (graph) for the given tag.
    
    source: Identifier for the start node in graph
    
    sink: Identifier for the end node in graph

    graph: A NetworkX DiGraph

    tag: A tag identifier that defines which attribute in graph should
    be used as trust ratings in the calculation (DiGraph[x][y][tag] = rating)
    
    Returns: A dict containing the results, with keywords trust, threshold,
    paths_used, nodes_used, nodes_unused, source, sink, tag.
    
    """
    results = {"trust": None,
               "threshold": None,
               "paths_used": [],
               "nodes_used": [],
               "nodes_unused": [],
               "source": source,
               "sink": sink,
               "tag": tag,
               }
    
    # Remove all edges but the ones with the specific tag so that all_shortest_paths
    # gives correct paths. 
    try:
        remove_list = [(x,y) for (x,y) in graph.edges() if tag not in graph[x][y]]
    except AttributeError:
        print "(tidaltrust) AttributeError"
        raise TypeError("Input graph is probably not a compatible graph object.")
        
    graph.remove_edges_from(remove_list)

    try:
        shortest = nx.all_shortest_paths(graph, source=source, target=sink)
        paths_list = list(shortest)
    except nx.exception.NetworkXNoPath:
        print "(tidaltrust) No paths found between %s and %s." % (str(source), str(sink))
        return results
    except KeyError, e:
        # An input node was not in the graph 
        print "(tidaltrust) keyerror: %s" % (str(e))
        return results

    threshold = get_threshold(paths_list, graph, tag)
    results['threshold'] = threshold

    useful_paths = remove_low_rated_paths(paths_list, threshold, graph, tag)
    results["paths_used"] = useful_paths
    results["nodes_used"] = list(set(chain.from_iterable(useful_paths)))

    # Add unused nodes (not in shortest path) to results
    path_nodes = set(chain.from_iterable(useful_paths))
    results["nodes_unused"] += [n for n in graph.nodes() if n not in path_nodes]
    
    queue = []
    # Loop over all nodes in all paths that are not the sink or parents of the sink (leaves)
    # Possible optimization: merge this loop with the cached_trust loop below
    for i in reversed(range(len(useful_paths[0])-2)):
        for j in range(len(useful_paths)):
            if(useful_paths[j][i] not in queue):
                # Add to queue for backwards search
                queue.append(useful_paths[j][i])
    
    cached_trust = {}
                
    #Initialize cached_trust for all leaves.
    for n in range(len(useful_paths)):
        # Select predecessors of sink in path n
        sink_neighbor = useful_paths[n][len(useful_paths[0])-2]   
        if (sink_neighbor, sink) not in cached_trust:
            cached_trust[(sink_neighbor, sink)] = graph[sink_neighbor][sink][tag]
            
        
    # Backwards search from sink to source. Starts at the parents of the leaves.
    while queue:
        current_node = queue.pop(0)    
        children = graph.successors(current_node) # Get all children of current_node
        numerator = float(0)
        denominator = float(0)
        
        # For each child of current_node:
        # Sum up the ratings of all relevant edges to the children (weight>=threshold)
        # multiplied by the child's cached trust rating of the sink.
        # Divide this by the sum of the childrens' cached trust ratings of the sink.
        
        # Note: If only one path exists from a node to the sink,
        # its child's trust in the sink will be used. This may give a false
        # impression of trust between the node and the sink since the trust
        # between the parent and its child is not considered.
        # (rating*cached_rating)/rating = cached_rating
        # ???
        for s in children:
            # Use edge if rating >= threshold and the successor has a cached trust to the sink.
            if (graph[current_node][s][tag] >= threshold and (s, sink) in cached_trust):
                if cached_trust[(s, sink)] >= 0:
                    numerator = (numerator + 
                                 graph[current_node][s][tag]*cached_trust[(s, sink)])
                    denominator = denominator + graph[current_node][s][tag]
        
        if denominator > 0:
            cached_trust[(current_node, sink)] = numerator / denominator                                
    
        # Sets trust to -1 if no children could be used (e.g., ratings below threshold)
        else:
            cached_trust[(current_node, sink)] = -1       
            results["nodes_unused"].append(current_node)
        
    
    if (source, sink) in cached_trust:
        results["trust"] = round(cached_trust[(source, sink)],1)
        if threshold == sys.maxint:
            results["threshold"] = results["trust"]

    return results        
    
def get_threshold(paths, graph, tag):
    """
    Calculates the threshold used to exclude paths in the TidalTrust algorihm. 
    Returns the maximum trust of the lowest trust in each individual path

    """
    threshold = 0
    
    for path in paths:
        min_path_weight = sys.maxint
        
        for i in range(len(path)-2):
            if graph[path[i]][path[i+1]][tag] < min_path_weight:
               min_path_weight = graph[path[i]][path[i+1]][tag]
        
        if min_path_weight > threshold:
            threshold = min_path_weight  

    return threshold

def remove_low_rated_paths(paths, threshold, graph, tag):
    """
    Removes paths from a list of paths that contains weights below the threshold.
    
    """
    relevant_paths = paths[:]
    for path in paths:
        for i in range(len(path)-2):
            if graph[path[i]][path[i+1]][tag] < threshold:
               relevant_paths.remove(path)
            continue
    
    return relevant_paths

def compute_trust(network, source, sink, decision=None, tag="weight"):
    """
    Computes the trust between the source and sink (strings) in network
    (NetworkX DiGraph).

    If a tag is specified, edges will be considered tagged with properties, like so:
    
    >>> DiGraph[1][2]["cooking"]
    5

    Otherwise, the edges will be considered weighted:

    >>> DiGraph[1][2]["weight"]
    5

    Args:
       *network* (DiGraph): The graph in which trust is to be computed.

       *source* (str): The name of the source node.

       *sink* (str): The name of the sink node.

    Kwargs:
       *decision* (iterable): A list of node identifiers (i.e. names or id's)
       for nodes that are not to be used in the trust calculation.

       *tag* (str): A tag name. Only edges/ratings under this tag will be used
       in the trust calculation.

    Returns:
       A dict containing the results, with keywords trust, threshold, paths_used,
       nodes_used, nodes_unused, source, sink::

          {
             "trust": (int);
             "threshold": (int),
             "paths_used": (list of lists of str),
             "nodes_used": (list of str),
             "nodes_unused": (list of str),
             "source": (str),
             "sink": (str),
             "tag": (str),
          }

    """
  
    #check input
    if network == None or source == None or sink == None:
        raise TypeError("Input parameters can't be None")

    network = deepcopy(network)

    # Ignore nodes as specified by decision
    if decision != None:
        network.remove_nodes_from(decision)
   
    trust_results = tidal_trust(graph=network, source=source, sink=sink, tag=tag)
    
    return trust_results

