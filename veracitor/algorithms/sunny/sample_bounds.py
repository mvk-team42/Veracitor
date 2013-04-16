# -*- coding: utf-8 -*-

"""
The algorithm used for probabilistic logic sampling in SUNNY (as described by Golbeck and Kuter (2010)).
Computes minimum and maximum probability of success by using a stochastic simulation. Success is in this case defined as being used in the trust evaluation done by SUNNY.

"""

import veracitor.database as db
from veracitor.database import globalNetwork
import networkx as nx
import random
import itertools
from numpy import array
import math

tag = "cooking"

def sample_bounds(bayesianNetwork, k=10):
    """
    # TODO Skriva om parameter-texterna :p
    bayesianNetwork: The nodes to calculate the sample bounds for
    k : Number of times the sampling loops. A higher value (theoretically) decreases the randomness of the sampling 
    
    """

    xmin_counter = 0
    xmax_counter = 0
    # TODO backwards BFS to set attributes in correct order
    for _ in range(k):
        nodes = bayesianNetwork.node
        for n in nodes:
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
                if rand <= min(set):
                    nodes[n]['xmin'] = 1
                    xmin_counter+=1
                else:
                    nodes[n]['xmin'] = 0
                if rand <= max(set):
                    nodes[n]['xmax'] = 1
                    xmax_counter+=1
                else:
                    nodes[n]['xmax'] = 0

    
    min_total = xmin_counter/k
    max_total = xmax_counter/k
    return (min_total,max_total)

                 # OUTLINE
                
                # if difference on extremes exist:
                #     formula 1 (note that sigma does not mean stddev in
                #            the formula. See text above formula!)
                
                # else:
                #     formula 2
                
                # TODO: Choose weights w1 to w4. Start with the values 
                # Kuter and Golbeck use: (w1, w2, w3, w4) = (0.7, 0.2, 0.1, 0.8)
                # (provided the best results in their experiments)
                

                # Probability set:
                # Calculate probability of all possible scenarios
                # for all parents. e.g. if you have two parents,
                # they can be {true,true},{false,false},
                # {true,false} and {false,true}.
                # This depends on their xmin and xmax values.
                # When all combinations have been calculated,
                # the min and max probabilities are the used ones.
                # They are used with the randomized r to calculate
                # xmin and xmax for the current node.
                #
                # So, we need a way to calculate all possible
                # permutations of probabilities.
                # Example:
                # "A" has parents "B" and "C" with:
                # xmin(B) = 0, xmax(B) = 1
                # xmin(C) = 0, xmax(C) = 1
                #
                # In this case, we need to check the probability of
                # A being true with all four possible combinations
                # of probabilities for B and C.


def get_probability_set(network, node):
    """
    TODO

    """
    probabilities = set()
    variants = [[[n, True],[n, False]] for n in network.nodes()]
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
    
def _getRandom():
    # TODO: Choose a random function       
    # random() is nicer (shorter), but returns [0,1), meaning it doesn't include 1,
    # which we technically should.
    # But it's about 1 in a billion that uniform(0,1) actually returns 1.

    #return random.random
    #return random.uniform(0,1)
    return 42
    
    
# TODO: Ta bort _stddev och _mean. Flyttade till globalNetwork
def _stddev(numbers):
    np_array = array(numbers)
    return np_array.std()

def _mean(numbers):
    np_array = array(numbers)
    return np_array.mean()    

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

    ## TODO: use something other than globalNetwork (for example a network
    ##       sent in by sunny? <@:-)-X--<
    overall_difference = globalNetwork.get_overall_difference(p1, p2, [tag])
    difference_on_extremes = globalNetwork.get_difference_on_extremes(p1, p2, [tag])
    max_difference = globalNetwork.get_max_rating_difference(p1, p2, [tag])
    belief_coefficient = globalNetwork.get_belief_coefficient(p1, p2, [tag])

    print "overall_difference: " + str(overall_difference)
    print "diff on extremes: " + str(difference_on_extremes)
    print "max_difference " + str(max_difference)
    print "belief_coefficient: " + str(belief_coefficient)

    if difference_on_extremes is None:
        return belief_coefficient * \
            math.fabs(1 - 2 * (weights[3]*overall_difference + \
                                   (1 - weights[3])*max_difference)) 
    else:
        return belief_coefficient* \
            math.fabs(1 - 2 * (weights[0]*overall_difference + \
                                   weights[1]*max_difference + \
                                   weights[2]*difference_on_extremes))
    





