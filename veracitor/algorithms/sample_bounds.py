"""
The algorithm used for probabilistic logic sampling in SUNNY (as described by Golbeck and Kuter (2010)).
Computes minimum and maximum probability of success by using a stochastic simulation. Success is in this case defined as being used in the trust evaluation done by SUNNY.

"""

import random
from numpy import array
import itertools



def sample_bounds(bayesianNetwork, k=100):
    """
    # TODO Skriva om parameter-texterna :p
    bayesianNetwork: The nodes to calculate the sample bounds for
    k : Number of times the sampling loops. A higher value (theoretically) decreases the randomness of the sampling 
    
    """
    # Fast way to iterate k times when an index variable isn't needed according to http://stackoverflow.com/a/2970789/645270 (see comment too)
    # See simpler alternative below.
    for _ in itertools.repeat(None, k):
        print k
        
        
    # Simpler alternative to the above loop 
    #for _ in range(k):
        #print k
    
    
    
    
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
