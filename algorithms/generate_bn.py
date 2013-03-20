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

    It's probably slower than golbeck_generate_bn() and not guaranteed to
    return the same graph as a golbeck_generate_bn would given the same
    input, but it does the job of minimizing the input network by finding
    all paths from source to sink.

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
    TODO: Finish

    """
    K = set(graph.predecessors(sink))
    KK = set()

    while K != KK and source not in K:
        KK = K.copy()
        K_has_changed = True
        while K_has_changed:
            pre_img = _pre_img(K, graph, tag)
            if len(pre_img) = 0:
                K_has_changed = False
            else:
                K = K | pre_img
                
        # Remove cycles, redundant nodes etc and store only the nodes
        # relevant (those that lie in a path from source to sink)
        K = _prune_states(K, graph, source, sink)

    K.add(sink)
                
    
    # Return a the subgraph of graph containing only the relevant nodes
    return graph.subgraph(list(K))

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
    # TODO: This is not a correct implementation
    # Create a subgraph with the nodes now in K
    subgraph = graph.subgraph(list(K))

    # Get all paths from source to sink without cycles and redundant nodes
    simple_paths_gen = nx.all_simple_paths(G=subgraph, source=source, target=sink)

    # Make a set of all nodes in the relevant paths
    relevant_nodes = set(chain.from_iterable(simple_paths_gen))
    
    return relevant_nodes
