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

tag = "cooking"

def sample_bounds(bayesianNetwork, source, sink, k=10):
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
            if not bayesianNetwork.successors(n):
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
                probability_set = get_probability_set(bayesianNetwork, n)
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

    
    min_total_source = xmin_counters[source]/k
    max_total_source = xmax_counters[source]/k
    return (min_total_source,max_total_source)



def get_probability_set(network, node):
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
            p_value = p_confidence(node,n)
            if xmax:
                m1 = nodes[n]['xmax']
                m2 = nodes[n]['xmin']
            else:
                m1 = nodes[n]['xmin']
                m2 = nodes[n]['xmax']
            product = product*(1-(m1*p_value + m2*(1-p_value)))
        probabilities.add(1-product)

    return probabilities
    
def p_confidence(p1, p2, weights=(0.7, 0.2, 0.1, 0.8)):
    """
    Implementation of *Equation (1)* from *Kuter, Golbeck 2010*. 

    Args:
       *p1, p2 (node identifiers)*: The nodes to calculate confidence
       between.

    Kwargs:
       *weights (tuple)*: The weights to be used in the equation. Default
       is the example weights from *Kuter, Golbeck 2010*.

    Returns:
       Returns the confidence ``P(p1|p2)``.
       
    """

    ## TODO: use something other than networkModel (for example a network
    ##       sent in by sunny? <@:-)-X--<
    overall_difference = networkModel.get_overall_difference(p1, p2, [tag])
    difference_on_extremes = networkModel.get_difference_on_extremes(p1, p2, [tag])
    max_difference = networkModel.get_max_rating_difference(p1, p2, [tag])
    belief_coefficient = networkModel.get_belief_coefficient(p1, p2, [tag])

    # TODO remove prints.
    #print "overall_difference: " + str(overall_difference)
    #print "diff on extremes: " + str(difference_on_extremes)
    #print "max_difference " + str(max_difference)
    #print "belief_coefficient: " + str(belief_coefficient)

    if difference_on_extremes is None:
        return belief_coefficient * \
            math.fabs(1 - 2 * (weights[3]*overall_difference + \
                                   (1 - weights[3])*max_difference)) 
    else:
        return belief_coefficient* \
            math.fabs(1 - 2 * (weights[0]*overall_difference + \
                                   weights[1]*max_difference + \
                                   weights[2]*difference_on_extremes))
