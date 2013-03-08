""" 
TidalTrust!

"""

import sys
import networkx as nx
import matplotlib.pyplot as plt


G = nx.DiGraph()
"""
G.add_weighted_edges_from([(1,2,10),3
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
    def tidal_trust(source, sink, graph):
        """ Calculates a trust value between the source and the sink nodes in the given graph """
        
        # TODO: throws networkx.exception.NetworkXNoPath. Handle?
        shortest = nx.all_shortest_paths(graph, source=source, target=sink)
        paths_list = list(shortest)
        threshold = TidalTrust.get_threshold(paths_list, graph)
        
        queue = []
        # Possible optimization: merge this loop with the cached_trust loop below
        # Loop over all nodes in all paths that are not the sink or predecessors to the sink (leaves)
        for i in reversed(range(len(paths_list[0])-2)):
            for j in range(len(paths_list)):
                if(paths_list[j][i] not in queue):
                    # Add to queue for backwards search
                    queue.append(paths_list[j][i])
        
        cached_trust = {}
        
        #Initialize cached_trust for all leaves.
        for n in range(len(paths_list)):
             # Select predecessors of sink in path n
            sink_neighbor = paths_list[n][len(paths_list[0])-2]   
            if (sink_neighbor, sink) not in cached_trust:
                cached_trust[(sink_neighbor, sink)] = graph[sink_neighbor][sink]['weight']
        
        
        # Backwards search from sink to source. Starts at the predecessors to the leaves.
        while queue:
            # Pop the first element 
            current_node = queue.pop(0)    
            # Get all children of current_node
            children = graph.successors(current_node)    
            numerator = float(0)
            denominator = float(0)

            # For each child of current_node:
            # Sum up the ratings of all relevant edges to the children (weight>=threshold)
            # multiplied by the child's cached trust rating of the sink sink.
            # Divide this by the sum of the childrens cached trust ratings of the sink.

            for s in children:
                # Use edge if rating >= threshold and the successor has a cached trust to the sink.
                if (graph[current_node][s]['weight'] >= threshold and (s, sink) in cached_trust):
                        if cached_trust[(s, sink)] >= 0:
                            numerator = (numerator + 
                                graph[current_node][s]['weight']*cached_trust[(s, sink)])
                            denominator = denominator + graph[current_node][s]['weight']
            
            if denominator > 0:
                cached_trust[(current_node, sink)] = numerator / denominator                                
            else:
                cached_trust[(current_node, sink)] = -1       
        
        if (source, sink) in cached_trust:
            return cached_trust[(source, sink)]
        else:
            return None    # TODO: Raise exception here???
    
    
    @staticmethod    
    def get_threshold(paths, graph):
        """ Calculates the threshold used to exclude paths in the TidalTrust algorithm. 
            Returns the maximum trust of the lowest trust in each individual path """
        threshold = 0
        
        for path in paths:
            min_path_weight = sys.maxint
            
            for i in range(len(path)-2):
                if graph[path[i]][path[i+1]]['weight'] < min_path_weight:
                   min_path_weight = graph[path[i]][path[i+1]]['weight']
            
            if min_path_weight > threshold:
                threshold = min_path_weight  
                           
        return threshold
        
    # possible optimization?: use this
    @staticmethod
    def remove_low_rated_paths(paths, threshold, graph):
        """ Removes paths from a list of paths that contains weights below the threshold """
        relevant_paths = paths[:]
        for path in paths:
            for i in range(len(path)-2):
                if graph[path[i]][path[i+1]]['weight'] < threshold:
                   relevant_paths.remove(path)
                break
        
        return relevant_paths
        
        #nx.draw(graph)
        #nx.draw_circular(graph)
        #nx.draw_spectral(graph)
        #plt.show()
    
    

     

