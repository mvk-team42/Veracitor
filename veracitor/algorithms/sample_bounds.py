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



def sample_bounds(bayesianNetwork, k=10):
    """
    # TODO Skriva om parameter-texterna :p
    bayesianNetwork: The nodes to calculate the sample bounds for
    k : Number of times the sampling loops. A higher value (theoretically) decreases the randomness of the sampling 
    
    """
    sample_size = 0
    for _ in range(k):
        sample_size+=1
        nodes = bayesianNetwork.node
        for n in nodes:
            if not bayesianNetwork.predecessors(n):
                if not 'decision' in n: 
                    n['xmin'] = 0
                    n['xmax'] = 1
                elif n['decision']:
                    n['xmin'] = 1
                    n['xmax'] = 1
                else: 
                    n['xmin'] = 0
                    n['xmax'] = 0
                    
            else:
                
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


                #print str(globalNetwork.get_global_network())
                #print globalNetwork.get_global_network()['DN']
                #print nx.to_dict_of_dicts(globalNetwork.get_global_network())
                #globalNetwork.get_common_info_ratings(n, bayesianNetwork.predecessors(n)[0], ['crime'])

                pass

    globaln = globalNetwork.get_global_network()
    print globalNetwork.get_common_info_ratings("1", "2", ["gardening"])
                    
    
    
def _getRandom():
    # TODO: Choose a random function       
    # random() is nicer (shorter), but returns [0,1), meaning it doesn't include 1, which we technically should.
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
