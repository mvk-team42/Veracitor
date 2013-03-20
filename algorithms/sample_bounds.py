"""
The algorithm used for probabilistic logic sampling in SUNNY (as described by Golbeck and Kuter (2010)).
Computes minimum and maximum probability of success by using a stochastic simulation. Success is in this case defined as being used in the 
trust evaluation done by SUNNY.

"""

import random
from numpy import array



def sample_bounds():
    pass
    
    
    
    
def _getRandom():
    # TODO: Välja någon random-funktion.        
    # random() är snyggare (kortare), men ger [0,1), dvs inkluderar inte 1, vilket vi tekniskt sett ska göra.
    # Däremot är chansen typ 1 på 100 miljarder att den faktiskt blir 1 i uniform(0,1) :p

    #return random.random
    #return random.uniform(0,1)
    return 42
    
    
    
def _stddev(numbers):
    np_array = array(numbers)
    return np_array.std()

def _mean(numbers):
    np_array = array(numbers)
    return np_array.mean()    