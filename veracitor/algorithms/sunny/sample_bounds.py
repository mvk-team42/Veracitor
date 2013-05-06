# -*- coding: utf-8 -*-

"""
.. module:: sample_bounds
    :synopsis: The algorithm used for probabilistic logic sampling in SUNNY (as described by Golbeck and Kuter (2010)).
Computes minimum and maximum probability of success by using a stochastic simulation. Success is in this case defined as being used in the trust evaluation done by SUNNY.

.. moduleauthor:: Daniel Molin <dmol@kth.se>
.. moduleauthor:: Martin Runelöv <mrunelov@kth.se>
"""

import veracitor.database as db
from veracitor.database import networkModel
import networkx as nx
import random
import itertools
from numpy import array
import math

def sample_bounds(bayesianNetwork, source, sink, bounds, p_conf, tag, k=10):
    """
    The main function in the sampling procedure. 

    bayesianNetwork : The nodes to calculate the sample bounds for

    k : Number of sampling iterations. A higher value (theoretically) decreases the randomness of the sampling.

    source : The source node from SUNNY.

    sink : The sink node from SUNNY. Used to topologically sort the network
    
    Returns: A tuple containing the lower and upper bounds for the source node
    """

    xmin_counters = {}
    xmax_counters = {}
    for n in bayesianNetwork.nodes():
        xmin_counters[n] = 0
        xmax_counters[n] = 0
    for _ in range(k):
        nodes = bayesianNetwork.node
        # Top sort the nodes to traverse parents before children
        top_sort_nodes = nx.topological_sort(bayesianNetwork.reverse(),[sink])
        for n in top_sort_nodes:
            if n in bayesianNetwork.successors(sink):
                if not 'decision' in nodes[n]: 
                    nodes[n]['xmin'] = 0
                    nodes[n]['xmax'] = 1
                elif n['decision']:
                    nodes[n]['xmin'] = 1
                    nodes[n]['xmax'] = 1
                else: 
                    nodes[n]['xmin'] = 0
                    nodes[n]['xmax'] = 0
                    
            else:
                parents = bayesianNetwork.successors(n)
                # If this is the first run, calculate probabilities
                if not bounds:
                    probability_set = get_probability_set(bayesianNetwork, n, tag, p_conf)
                # Else, use the previously sampled probabilities
                else:
                    probability_set = set([bounds[n]])
                rand = random.random()
                if rand <= min(probability_set):
                    nodes[n]['xmin'] = 1
                    xmin_counters[n]+=1
                else:
                    nodes[n]['xmin'] = 0
                if rand <= max(probability_set):
                    nodes[n]['xmax'] = 1
                    xmax_counters[n]+=1
                else:
                    nodes[n]['xmax'] = 0
    
    # Build the return value.
    if not bounds:
        for node in bayesianNetwork.node:
            bounds[node] = [xmin_counters[node]/k, xmax_counters[node]/k]
    else:
        bounds[source] = [xmin_counters[source]/k, xmax_counters[source]/k]

    return bounds



def get_probability_set(network, node, tag, p_conf):
    """
    Calculates the set of possible probabilites of 'node' being true (included). 

    """
    probabilities = set()
    # Generates all possible permutations of xmin and xmax values
    # for the current node and its parents
    variants = [[[n, True],[n, False]] for n in network.successors(node)]
    permutations = list(itertools.product(*variants))
    nodes = network.node
    for p in permutations:
        product = 1
        for (n,xmax) in p:
            p_value = p_conf[(node,n,tag)]
            if xmax:
                m1 = nodes[n]['xmax']
                m2 = nodes[n]['xmin']
            else:
                m1 = nodes[n]['xmin']
                m2 = nodes[n]['xmax']
            product = product*(1-(m1*p_value + m2*(1-p_value)))
        probabilities.add(1-product)

    return probabilities
