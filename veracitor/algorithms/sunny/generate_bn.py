# -*- coding: utf-8 -*-

"""
The algorithm for generating a probabilistic network, given a trust network,
graph, and two nodes, source and sink (as described by Golbeck and Kuter (2010))

.. note:
   From *Kuter, Golbeck 2010*: 
   The nodes in K returned by GENERATEBN and the edges between those nodes
   constitute the probabilistic network BT as follows. For each node n in K, we
   define a Boolean variable x that denotes the logical proposition that whether n
   believes in the sink node n∞. In BT , X is the set of such logical propositions. A
   is the set of all of the edges between the nodes in K, with the directions of those
   edges reversed. Then, we use Equation (1) in order to compute the conditional
   probabilities for every edge in BT .

"""

import networkx as nx
from itertools import chain
from veracitor.database import networkModel
import math

def golbeck_generate_bn(graph, source, sink, tag="weight"):
    """
    GenerateBN as described by Golbeck and Kuter (2010).

    Implements Prune-States by first eliminating cycles found by
    nx.simple_cycles and removing the edge between the second last and last
    node in all cycles and then running nx.all_simple_paths to find only
    the relevant nodes left after all cycles have been destroyed.

    Returns not a true subgraph of the input graph, but a subgraph with some
    edges removed (e.g., "internal" cycles) and all remaining edges reversed,
    and a dict of all conditional probabilities calculated with *Equation (1)*
    from *Golbeck and Kuter (2010)*.
    
    Args:
       *graph* (networkX.DiGraph): A trust network.
      
       *source* (str): The source node identifier.

       *sink* (str): The sink node identifier

    Kwargs:
       *tag* (str): The tag specifying which ratings should be considered.

    Returns:
       A tuple::

          (BN (networkX.DiGraph), p_conf (dict))

       *BN* is more or less a bayesian network generated from the input graph,
       with all edges reversed. *p_conf* is a dictionary of all probabilistic
       confidence values (see *Equation (1)*) looking like this::
       
          {
             (A (str), B (str), tag (str)): P (float),
          }

       where *A* and *B* are nodes for which *P* is the confidence value 
       calculated from their decisions on information objects under the
       tag *tag*.
   
    """
    graph.remove_edges_from([(sink,y) for y in graph.successors(sink)])
    K = set(graph.predecessors(sink))
    KK = set()
    Kgraph = graph.subgraph(list(K)+[sink]) # makes it work if source and sink are neighbours

    while K != KK and source not in K:
        KK = K.copy()
        K_has_changed = True
        while K_has_changed:
            pre_img = _pre_img(K, graph, tag)
            if len(pre_img) == 0:
                K_has_changed = False
            else:
                K = K | pre_img

        # Remove cycles, redundant nodes etc and store only the 
        # relevant nodes 
        # (those that lie in a path from source to sink)
        K.add(sink)        
        Kgraph = _prune_states(K, graph, source, sink)
        K = set(Kgraph.nodes())

    # Reverse the edges to calc conditional probs
    Kgraph = Kgraph.reverse()

    # Calculate conditional probabilities
    cond_probs = _p_confidence(Kgraph, tag)
    # the relevant nodes and edges
    return (Kgraph, cond_probs)

def _pre_img(K, graph, tag):
     """
     pre_img(K, graph, tag) =
         set({n | n is a node in graph, n not in K, n' in K and graph[n][n'][tag] != 0}).

     (Returns a set of nodes that lie outside of K but have neighbours in K.)

     """
     return set([x for (x, y) in graph.edges()
                 if y in K and
                 graph[x][y][tag] != 0
                 and x not in K])

def _prune_states(K, graph, source, sink):
    """
    Removes cycles and redundant nodes (that are not reachable from source)
    from the subgraph of graph defined by the nodes in K.
    
    """
    
    # Create a subgraph with the nodes now in K
    # Find and remove cycles by deleting the edge between 
    # the second to last node and the last node of the cycle,
    # thus keeping nodes that may be important 
    # to the trust calculation.
    subgraph = graph.subgraph(K)
    cycles = nx.simple_cycles(subgraph)
    if cycles:
        for cycle in cycles:
            subgraph.remove_edges_from([(cycle[-2], cycle[-1])])
            
    # Get all paths from source to sink without cycles and redundant nodes
    simple_paths = list(nx.all_simple_paths(G=graph, source=source, target=sink))
    relevant_nodes = set(chain.from_iterable(simple_paths))
            
    # Remove nodes no longer used (not in simple_paths)
    for n in K:
        if n not in relevant_nodes:
            subgraph.remove_node(n)
            
    return subgraph

def _p_confidence(graph, tag, weights=(0.7, 0.2, 0.1, 0.8)):
    """
    Implementation of *Equation (1)* from *Kuter, Golbeck 2010*. Calculates
    the conditional probablities following all edges in the input
    graph.

    Args:
       *graph (networkX DiGraph)*: The graph to calculate conditional
       probabilities for.

    Kwargs:
       *weights (tuple)*: The weights to be used in the equation. Default
       is the example weights from *Kuter, Golbeck 2010*.

    Returns:
       Returns a dict with the the conditional confidence probabilities for
       nodes.
       
       The dict will look like this::
          
          {
             (A, B, tag): probability (float), 
          }

       where A and B are nodes for which an edge A -> B exists in the graph,
       with a rating for the tag.
       
    """
    return_dict = {}

    for edge in graph.edges():
        p1, p2 = edge[0], edge[1]
        overall_difference = networkModel.get_overall_difference(p1, p2, [tag])
        difference_on_extremes = networkModel.get_difference_on_extremes(p1, p2, [tag])
        max_difference = networkModel.get_max_rating_difference(p1, p2, [tag])
        belief_coefficient = networkModel.get_belief_coefficient(p1, p2, [tag])
            
        if difference_on_extremes is None:
            return_dict[(p1, p2, tag)] =  belief_coefficient * \
                math.fabs(1 - 2 * (weights[3]*overall_difference + \
                                       (1 - weights[3])*max_difference)) 
        else:
            return_dict[(p1, p2, tag)] = belief_coefficient* \
                math.fabs(1 - 2 * (weights[0]*overall_difference + \
                                       weights[1]*max_difference + \
                                       weights[2]*difference_on_extremes))

    return return_dict
            
