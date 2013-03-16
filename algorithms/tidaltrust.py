""" 
TidalTrust!

"""

import sys
import networkx as nx
import matplotlib.pyplot as plt

class TidalTrust:
    
    @staticmethod
    def tidal_trust(source, sink, graph, tag):
        """ 
        Calculates a trust value between the source and the sink nodes 
        in the given graph for the given tag 
        
        """
        
        # TODO: throws networkx.exception.NetworkXNoPath. Handle?
        # Suggestion: 
        # Remove all edges but the ones with the specific tag so that all_shortest_paths
        # gives correct paths. If done like this, no tag specific commands are needed
        # either.
        # Code: 
        # remove_list = [(x,y) for (x,y) in Graph.edges() if 'crime' not in Graph[x][y]]
        # Graph.remove_edges_from(remove_list)
        
        shortest = nx.all_shortest_paths(graph, source=source, target=sink)
        paths_list = list(shortest)
        threshold = TidalTrust.get_threshold(paths_list, graph, tag)
        
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
                cached_trust[(sink_neighbor, sink)] = graph[sink_neighbor][sink][tag]
        
        
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

            # Note: If only one path exists from a node to the sink,
            # its child's trust in the sink will be used. This may give a false
            # impression of trust between the node and the sink since the trust
            # between the parent and its child is not considered.
            # (rating*cached_rating)/rating = cached_rating
            # ???
            for s in children:
                # Use edge if rating >= threshold and the successor has a cached trust to the sink.
                if (graph[current_node][s][tag] >= threshold and (s, sink) in cached_trust):
                        if cached_trust[(s, sink)] >= 0:
                            numerator = (numerator + 
                                graph[current_node][s][tag]*cached_trust[(s, sink)])
                            denominator = denominator + graph[current_node][s][tag]
            
            if denominator > 0:
                cached_trust[(current_node, sink)] = numerator / denominator                                
            else:
                cached_trust[(current_node, sink)] = -1       
        
        if (source, sink) in cached_trust:
            return cached_trust[(source, sink)]
        else:
            return None    # TODO: Raise exception here???
    
    
    @staticmethod    
    def get_threshold(paths, graph, tag):
        """ Calculates the threshold used to exclude paths in the TidalTrust algorithm. 
            Returns the maximum trust of the lowest trust in each individual path """
        threshold = 0
        
        for path in paths:
            min_path_weight = sys.maxint
            
            for i in range(len(path)-2):
                if graph[path[i]][path[i+1]][tag] < min_path_weight:
                   min_path_weight = graph[path[i]][path[i+1]][tag]
            
            if min_path_weight > threshold:
                threshold = min_path_weight  

        return threshold
        
    # possible optimization?: use this
    # users beware for this code is old 
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

    @staticmethod
    def compute_trust(bayesianNetwork, source, sink, decision=None, tag=None):
        """
        Computes the trust between the source and sink in a graph (bayesianNetwork) 
        and returns the value as a float.

        decision (optional): A list of node identifiers (i.e. names or id's) for
        nodes that are not to be used in the trust calculation.

        tag (optional): A tag name (String). Only edges/ratings under this tag
        will be used in the trust calculation.

        If tag is specified, edges will be tagged with properties, like so:
        G[1][2][tag_name] = rating.
        Otherwise, the edges will be considered weighted: G[1][2]["weight"] = rating
        """
        # Ignore nodes as specified by decision
        if decision != None:
            for node in decision:
                bayesianNetwork.remove_node(node)
        if tag == None:
            tag = "weight"

<<<<<<< HEAD
<<<<<<< HEAD
        return TidalTrust.tidal_trust(graph=bayesianNetwork, source=source, sink=sink, tag=tag)
=======
        return TidalTrust.tidal_trust(graph=bayesianNetwork, source=source, sink=sink, tag="weight")
>>>>>>> Better edge formats
=======
        return TidalTrust.tidal_trust(graph=bayesianNetwork, source=source, sink=sink, tag=tag)

>>>>>>> Changed the format of edges - tags are now properties at the same level as the 'weight' property and so everything now works as we wanted. See related Issue for more info

        






    


     

