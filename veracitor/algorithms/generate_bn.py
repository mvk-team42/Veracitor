"""
The algorithm for generating a probabilistic network, given a trust network, graph, and two
nodes, source and sink (as described by Golbeck and Kuter (2010))

"""

import networkx as nx
from itertools import chain

def networkx_generate_bn(graph, source, sink, tag="weight", cutoff=None):
    """
    Provides an alternative to GenerateBN (Golbeck and Kuter, 2010) that
    implements NetworkX functions rather than the pseudo-code published in
    the paper.

    It's A LOT slower than golbeck_generate_bn() and not guaranteed to
    return the same graph as a golbeck_generate_bn would given the same
    input, but it does the job of minimizing the input network by finding
    all paths from source to sink.

    Use only for small graphs.

    """
    # Get all paths from source to sink without cycles and redundant nodes
    simple_paths_gen = nx.all_simple_paths(G=graph, source=source, target=sink)

    # Make a set of all nodes in the relevant paths
    relevant_nodes = set(chain.from_iterable(simple_paths_gen))

    # Return a subgraph consisting of the relevant nodes   
    return graph.subgraph(relevant_nodes)

def golbeck_generate_bn(graph, source, sink, tag="weight"):
    """
    GenerateBN as described by Golbeck and Kuter (2010).
    Probably faster than networkx_generate_bn().

    Implements Prune-States by first eliminating cycles found by
    nx.simple_cycles and removing the edge between the second last and last
    node in all cycles and then running nx.all_simple_paths to find only
    the relevant nodes left after all cycles have been destroyed.

    Returns not a true subgraph of the input graph, but a subgraph with some
    edges removed (e.g., "internal" cycles).
   
    """
    K = set(graph.predecessors(sink))
    KK = set()
    Kgraph = graph.subgraph(list(K)+[sink]) # makes it work if source and sink are neigbours

    while K != KK and source not in K:
        KK = K.copy()
        K_has_changed = True
        while K_has_changed:
            pre_img = _pre_img(K, graph, tag)
            if len(pre_img) == 0:
                K_has_changed = False
            else:
                K = K | pre_img

        # Remove cycles, redundant nodes etc and store only the nodes
        # relevant (those that lie in a path from source to sink)
        K.add(sink)        
        Kgraph = _prune_states(K, graph, source, sink)
        K = set(Kgraph.nodes())
    
    # Return a subgraph of graph containing only
    # the relevant nodes and edges
    return Kgraph

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
    subgraph = graph.subgraph(list(K))
    
    # Find and remove cycles by deleting the edge between the second to last
    # node and the last node of the cycle, thus keeping nodes that may be
    # important to the trust calculation.
    cycles = nx.simple_cycles(subgraph)
    if cycles:
        for cycle in cycles:
            subgraph.remove_edges_from([(cycle[-2], cycle[-1])])
            
    # Get all paths from source to sink without cycles and redundant nodes
    simple_paths = list(nx.all_simple_paths(G=subgraph, source=source, target=sink))
    relevant_nodes = set(chain.from_iterable(simple_paths))
            
    # Remove nodes no longer used (not in simple_paths)
    for n in K:
        if n not in relevant_nodes:
            subgraph.remove_node(n)
            
    return subgraph
