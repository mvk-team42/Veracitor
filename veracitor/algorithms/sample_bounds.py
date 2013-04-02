"""
The algorithm used for probabilistic logic sampling in SUNNY (as described by Golbeck and Kuter (2010)).
Computes minimum and maximum probability of success by using a stochastic simulation. Success is in this case defined as being used in the trust evaluation done by SUNNY.

"""

from veracitor.database import *
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
                print "RUNNING get_common_info_ratings"
                get_common_info_ratings(n, n.predecessors(0))
                    
    
    
def _getRandom():
    # TODO: Choose a random function       
    # random() is nicer (shorter), but returns [0,1), meaning it includes 1, which we technically shouldn't.
    # But it's about 1 in a billion that uniform(0,1) actually returns 1.

    #return random.random
    #return random.uniform(0,1)
    return 42
    
    
    
def _stddev(numbers):
    np_array = array(numbers)
    return np_array.std()

def _mean(numbers):
    np_array = array(numbers)
    return np_array.mean()    
