""" 
TidalTrust!

"""

import sys
import networkx as nx
from itertools import tee, izip
import matplotlib.pyplot as plt

G = nx.DiGraph()
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



class TidalTrust:


    
    @staticmethod
    def tidal_trust(source=None, sink=None, graph=None):
        """ Calculates a trust value between the source and the sink nodes in the given graph """
        
        shortest = nx.all_shortest_paths(G, source=1, target=7)
        paths_list = list(shortest)
        threshold = TidalTrust.get_threshold(paths_list)
        
        queue = []
        for i in reversed(range(len(paths_list[0]))):
            for j in range(len(paths_list)):
                if(paths_list[j][i] not in queue):
                    queue.append(paths_list[j][i])
                    
        print queue
        
        #relevant_paths = TidalTrust.remove_low_rated_paths(paths_list,threshold)
        #print paths_list
        return 0
     
    
    @staticmethod    
    def get_threshold(paths):
        """ Calculates the threshold used to exclude paths in the TidalTrust algorithm. Returns max(min(weight(x,y))) """
        threshold = 0
        
        for path in paths:
            min_path_weight = sys.maxint
            
            for i in range(len(path)-1):
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
    
    

     

