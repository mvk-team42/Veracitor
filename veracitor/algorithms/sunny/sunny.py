# -*- coding: utf-8 -*-

"""
.. module:: sunny
:synopsis: The SUNNY algorithm as specified by Golbeck and Kuter (2010).

.. moduleauthor:: Daniel Molin <dmol@kth.se>
.. moduleauthor:: Martin Runelov <mrunelov@kth.se>
"""

from veracitor.algorithms import tidaltrust as tt
from generate_bn import golbeck_generate_bn as generate_bn
from sample_bounds import sample_bounds

def sunny(graph, source, sink, tag="weight"):
    """
    Decides which nodes to include using logic sampling in sample_bounds,
    then calculates a trust value between the source and the sink nodes using 
    the TidalTrust algorithm.

    Specified in *Kuter, Golbeck (2010)*.
    
    Args:
       source (str): Identifier for the start node in graph
    
       sink (str): Identifier for the end node in graph
    
       graph (networkX.DiGraph): The trust network
    
    Kwargs:
       tag (str): A tag identifier that defines which attribute in graph
       should be used as trust ratings in the calculation (DiGraph[x][y][tag] = rating)
    
    Returns:
       A dict containing the results, with keywords trust, threshold,
       paths_used, nodes_used, nodes_unused, source, sink, tag.
        
    """
    epsilon = 0.2
    # List of nodes to exclude
    decision = []
    bayesianNetwork,p_conf = generate_bn(graph,source,sink,tag)
    # TODO: leaves are the ones with out_degree 0 after the flip in generate_bn, right? Otherwise, in_degree = 0?
    bounds = sample_bounds(bayesianNetwork, source, sink, {}, p_conf, tag, 100)
    source_lower = bounds[source][0]
    source_upper = bounds[source][1]

    leaves = bayesianNetwork.successors(sink)
    for leaf in leaves:
        bayesianNetwork[leaf]['decision'] = True
        bounds = sample_bounds(bayesianNetwork, source, sink, bounds, p_conf, tag, 100)
        if not abs(bounds[source][0] - source_lower) < epsilon and abs(bounds[source][1] - source_upper) < epsilon:
            decision.append(leaf)
            bayesianNetwork[leaf]['decision'] = False
        else:
            bayesianNetwork[leaf]['decision'] = True

    return tt.compute_trust(bayesianNetwork, source, sink, decision, tag)

    

