""" 
TidalTrust!

"""

import sys
import networkx as nx
from itertools import tee, izip
import matplotlib.pyplot as plt


G = nx.DiGraph()
"""
G.add_weighted_edges_from([(1,2,10),
                           (1,3,8),
                           (1,4,9),
                           (2,5,9),
                           (3,5,10),
                           (3,6,10),
                           (4,5,8),
                           (4,6,9),
                           (5,7,8),
                           (6,7,6),
                           ])
""" 

"""
G.add_weighted_edges_from([(1,2,10)])                     
"""
G.add_weighted_edges_from([(1,2,8),
                           (1,3,5),
                           (1,4,3),
                           (2,4,4),
                           (3,4,7),
                           ])
                                   

class TidalTrust:
    
    @staticmethod
    def tidal_trust(source=None, sink=None, graph=None):
        """ Calculates a trust value between the source and the sink nodes in the given graph """
        
        source = 1
        sink = 4
        
        shortest = nx.all_shortest_paths(G, source=source, target=sink)    # TODO: throws networkx.exception.NetworkXNoPath. Handle?
        paths_list = list(shortest)
        threshold = TidalTrust.get_threshold(paths_list)
        
        queue = []
        for i in reversed(range(len(paths_list[0])-2)):    # Loop over all nodes in all paths that are not the sink or predecessors to the sink
            for j in range(len(paths_list)):
                if(paths_list[j][i] not in queue):
                    queue.append(paths_list[j][i])        # Add to queue for backwards search
        
        cached_trust = {}
        
        #Initialize cached_trust for all predecessors (children) to the sink.
        for n in range(len(paths_list)):
            sink_neighbor = paths_list[n][len(paths_list[0])-2]    # Select predecessors of sink in path n
            if (sink_neighbor, sink) not in cached_trust:
                cached_trust[(sink_neighbor, sink)] = G[sink_neighbor][sink]['weight']
        
        
        # Backwards search from sink to source. Starts at the predecessors to the predecessors of the sink.
        while queue:
            current_node = queue.pop(0)    # Pop the first element 
            successors = G.successors(current_node)    # Get all children pointing to current_node
            numerator = float(0)
            denominator = float(0)
            for s in successors:
                if G[current_node][s]['weight'] >= threshold:
                    if (s, sink) in cached_trust:
                        if cached_trust[(s, sink)] >= 0:
                            numerator = (numerator + 
                                G[current_node][s]['weight']*cached_trust[(s, sink)])
                            denominator = denominator + G[current_node][s]['weight']
            
            if denominator > 0:
                cached_trust[(current_node, sink)] = numerator / denominator                                
            else:
                cached_trust[(current_node, sink)] = -1       
        
        if (source, sink) in cached_trust:
            return cached_trust[(source, sink)]
        else:
            return None    # TODO: Raise exception here???
    
    
    @staticmethod    
    def get_threshold(paths):
        """ Calculates the threshold used to exclude paths in the TidalTrust algorithm. 
            Returns the maximum trust of the lowest trust in each individual path """
        threshold = 0
        
        for path in paths:
            min_path_weight = sys.maxint
            
            for i in range(len(path)-2):
                if G[path[i]][path[i+1]]['weight'] < min_path_weight:
                   min_path_weight = G[path[i]][path[i+1]]['weight']
            
            if min_path_weight > threshold:
                threshold = min_path_weight  
                           
        return threshold
        
    @staticmethod
    def remove_low_rated_paths(paths, threshold):
        """ Removes paths from a list of paths that contains weights below the threshold """
        relevant_paths = paths[:]
        for path in paths:
            for i in range(len(path)-2):
                if G[path[i]][path[i+1]]['weight'] < threshold:
                   relevant_paths.remove(path)
                break
        
        return relevant_paths
        
        #nx.draw(G)
        #nx.draw_circular(G)
        #nx.draw_spectral(G)
        #plt.show()
    
    

     

