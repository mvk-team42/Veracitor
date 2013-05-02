import unittest
import networkx as nx
import tidaltrust as tt
from sunny import generate_bn as gbn
from copy import copy, deepcopy
from random import randint
#import matplotlib.pyplot as plt

class TestTidalTrust(unittest.TestCase):
    def setup(self):
        pass
    
    def teardown(self):
        pass

    def test_parameters_constant(self):
        """
        (compute_trust) Input parameter objects are not changed

        """
        
        # Test for weighted graph
        G = _get_weighted_graph()
        source = 1
        sink = 7
        Gcopy = deepcopy(G)
        tt.compute_trust(G, source, sink)
        self.assertEqual(nx.to_dict_of_dicts(Gcopy),
                         nx.to_dict_of_dicts(G))
        self.assertEqual(7, sink)
        self.assertEqual(1, source)

        # Test for tagrated graph
        G = _get_tagrated_graph()
        Gcopy = deepcopy(G)
        tag = "cooking"
        tt.compute_trust(G, source, sink, tag=tag)
        self.assertEqual(nx.to_dict_of_dicts(Gcopy),
                         nx.to_dict_of_dicts(G))
        self.assertEqual(7, sink)
        self.assertEqual(1, source)
        self.assertEqual("cooking", tag)

        # Test with decision array
        decision = [5]
        tt.compute_trust(G, source, sink, tag="cooking", decision=decision)
        self.assertEqual(nx.to_dict_of_dicts(Gcopy),
                         nx.to_dict_of_dicts(G))
        self.assertEqual(7, sink)
        self.assertEqual(1, source)
        self.assertEqual([5], decision)
        
        
        # Test for graph with cycles
        G = _get_graph_with_cycles()
        Gcopy = deepcopy(G)
        tt.compute_trust(G, source, sink)
        self.assertEqual(nx.to_dict_of_dicts(Gcopy),
                         nx.to_dict_of_dicts(G))
        self.assertEqual(7, sink)
        self.assertEqual(1, source)

    def test_returns_none_when_no_paths(self):
        """
        (compute_trust) Return None when no trust value could be found

        """
        G = nx.DiGraph()
        G.add_nodes_from([1,2]) 
       
        # Test when there really is no path to begin with (no edges)
        self.assertIsNone(tt.compute_trust(G,1,2)["trust"])

        # Test when edges have the wrong tag
        G.add_edge(1,2,dict(cooking=4))
        self.assertIsNone(tt.compute_trust(G,1,2,tag="crime")["trust"])
        
        # Test when input nodes are not in the graph
        self.assertIsNone(tt.compute_trust(G,1,5,tag="crime")["trust"])
        self.assertIsNone(tt.compute_trust(G,7,2,tag="crime")["trust"])
        self.assertIsNone(tt.compute_trust(G,10,11,tag="crime")["trust"])

    def test_raises_exceptions_on_strange_input(self):
        """
        (compute_trust) Raises exceptions when input was objects of the wrong type

        """
        G = _get_tagrated_graph()

        # Test for None source/sink
        self.assertRaises(TypeError, tt.compute_trust, G, None, 7)
        self.assertRaises(TypeError, tt.compute_trust, G, 1, None)
        self.assertRaises(TypeError, tt.compute_trust, G, None, None)

        # Test for None graph
        self.assertRaises(TypeError, tt.compute_trust, None, 1, 7)
        
        # Test for when decision is not an iterable
        self.assertRaises(TypeError, tt.compute_trust, G, 1, 7, decision=unittest.TestCase)  
        
        # Test for bayesianNetwork does not work like graph
        self.assertRaises(TypeError, tt.compute_trust, "string", 1, 7)


    def test_dry_runs(self):
        """
        (compute_trust) Returns the same value as Tidal Trust would (i.e. the correct value)
        
        """
        #
        # Dry run 1:
        #
        # Threshold candidates = [9,8]. Threshold = max([9,8] = 9
        # 
        # Rating 1 -> 7:
        #     5 -> 7 = 8 (Direct trust value)
        #     6 -> 7 = 6 (Direct trust value)
        #     2 -> 7 = (9*8)/9 = 8
        #     3 -> 7 Invalid path since 1 -> 3 has a trust value below the Threshold.
        #     4 -> 7 = (4 -> 5 < Threshold. Not included) = (9*6)/9 = 6
        # 1 -> 7 = ((10*8) + 9*6))/(10+9) = 7.052631578947368 
        # (Calculated using python to get the same number of decimals)
        
        G = _get_badass_graph()
        self.assertEqual(tt.compute_trust(G,1,7)["trust"], 7.052631578947368)

        # Test trivial (direct edge source->sink)
        G = nx.DiGraph()
        G.add_edge(1,2,{"cooking":5})
        results = tt.compute_trust(G,1,2,tag="cooking")
        self.assertEqual(results["trust"], 5)

    def test_paths_used(self):
        """
        (compute_trust) paths_used in results are the actual used paths (if a trust value could be calculated)
        
        """
        # Test tagrated
        G = _get_tagrated_graph()
        results = tt.compute_trust(G,1,7,tag="cooking")
        self.assertEqual(results["paths_used"], [[1,2,5,7],[1,4,6,7]])

        # Test badass
        G = _get_badass_graph()
        results = tt.compute_trust(G,1,7)
        self.assertEqual(results["paths_used"], [[1,2,5,7],[1,4,6,7]])
        
        # Test small trivial
        G = nx.DiGraph()
        G.add_edge(1,2,{"cooking":5})
        results = tt.compute_trust(G,1,2,tag="cooking")
        self.assertEqual(results["paths_used"], [[1,2]])

    def test_nodes_used(self):
        """
        (compute_trust) nodes_used in results are the actually used nodes

        """
        # Test badass
        G = _get_badass_graph()
        results = tt.compute_trust(G,1,7)
        list.sort(results["nodes_used"])
        self.assertEqual(results["nodes_used"], [1,2,4,5,6,7])
        
        # Test small trivial
        G = nx.DiGraph()
        G.add_edge(1,2,{"cooking":5})
        results = tt.compute_trust(G,1,2,tag="cooking")
        list.sort(results["nodes_used"])
        self.assertEqual(results["nodes_used"], [1,2])

    def test_nodes_unused(self):
        """
        (compute_trust) nodes_unused in results are all unused nodes
        
        """
        # Test badass
        G = _get_badass_graph()
        results = tt.compute_trust(G,1,7)
        list.sort(results["nodes_unused"])
        self.assertEqual(results["nodes_unused"], [0,3,8,9])

        # No unused 
        G = nx.DiGraph()
        G.add_edge(1,2,{"cooking":5})
        results = tt.compute_trust(G,1,2,tag="cooking")
        list.sort(results["nodes_unused"])
        self.assertEqual(results["nodes_unused"], [])
        
    def test_source_sink_tag_return(self):
        """
        (compute_trust) Returns the same source, sink and tag that were put in

        """
        G = _get_tagrated_graph()
        results = tt.compute_trust(G,1,7,tag="cooking")
        self.assertEqual(results["source"],1)
        self.assertEqual(results["sink"],7)
        self.assertEqual(results["tag"],"cooking")
        

class TestGenerateBN(unittest.TestCase):
    """
    Tests the module generate_bn    
        
    """
    def test_cycle_removal(self):
        """
        (generate_bn) Removes cycles from graphs. 
        
        """
        G = _get_graph_with_cycles()
        loops = nx.simple_cycles(G)
        self.assertNotEqual(loops, [])
        G = gbn.golbeck_generate_bn(G, 1, 7)
        loops = nx.simple_cycles(G)
        self.assertEqual(loops, [])

        # Does not remove a cycle source -> sink -> source but that's not necessary I think
        G = _get_graph_with_cycles()
        G.add_edge(1,7,weight=10)
        G.add_edge(7,1,weight=10)
        G = gbn.golbeck_generate_bn(G, 1, 7)
        loops = nx.simple_cycles(G)
        self.assertNotEqual(loops, [])

    def test_source_sink_neighbours(self):
        """
        (generate_bn) Return a correct network when there is an edge source->sink

        """
        # Test for minimal trivial graph, should just return the same graph
        G = nx.DiGraph()
        G.add_weighted_edges_from([[0,1,1]])

        self.assertEqual(nx.to_dict_of_dicts(gbn.golbeck_generate_bn(G, 0, 1)), 
                         {0: {1:{'weight':1}}, 1: {}})

    def test_returns_correct_graph_when_source_sink_disconnected(self):
        """
        (generate_bn) Returs a graph with only the sink when there is no path source -> sink

        """
        G = _get_weighted_graph()
        G.remove_edges_from([(5,7),(6,7)])
        self.assertEqual(nx.to_dict_of_dicts(gbn.golbeck_generate_bn(G,1,7)), {7: {}})

    def test_parameters_constant(self):
        """
        (generate_bn) Input parameter objects are not changed

        """
        # Test for weighted graph
        G = _get_weighted_graph()
        source = 1
        sink = 7
        Gcopy = deepcopy(G)
        gbn.golbeck_generate_bn(G,1,7)
        self.assertEqual(nx.to_dict_of_dicts(Gcopy),
                         nx.to_dict_of_dicts(G))
        self.assertEqual(7, sink)
        self.assertEqual(1, source)

        # Test for tagrated graph
        G = _get_tagrated_graph()
        Gcopy = deepcopy(G)
        gbn.golbeck_generate_bn(G, source, sink, tag="cooking")
        self.assertEqual(nx.to_dict_of_dicts(Gcopy),
                         nx.to_dict_of_dicts(G))
        self.assertEqual(7, sink)
        self.assertEqual(1, source)


### HELP METHODS
def _get_weighted_graph():
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
    return G

def _get_tagrated_graph():
    Gtags = nx.DiGraph()
    Gtags.add_edges_from([(1,2,dict(cooking=10, crime=4, weight=10)),
                          (1,3,dict(cooking=8, crime=7, weight=8)),
                          (1,4,dict(cooking=9, crime=6, weight=9)),
                          (2,5,dict(cooking=9, crime=9, weight=9)),
                          (3,5,dict(cooking=10, crime=5, weight=10)),
                          (3,6,dict(cooking=10, crime=6, weight=10)),
                          (4,5,dict(cooking=8, crime=7, weight=8)),
                          (4,6,dict(cooking=9, crime=6, weight=9)),
                          (5,7,dict(cooking=8, crime=5, weight=8)),
                          (6,7,dict(cooking=6, crime=7, weight=6)),
                          ])
    return Gtags


def _get_graph_with_cycles():
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
                               (2,3,11),
                               (3,1,11),
                               (6,8,11),
                               (8,4,11),
                               ])      
    return G

def _get_badass_graph():
    """
    Same trust as _get_graph_with_cycles between 1 -> 7 but with cycles and useless nodes.    

    """
    G = _get_graph_with_cycles()
    G.add_edges_from([
            (7,1,{"cooking":10}), # edge sink -> source!
            (7,9,{"cooking":10}), # graph extends beyond sink
            (9,3,{"cooking":10}), # and back in again
            (0,1,{"cooking":10}),
            (1,1,{"cooking":10}), # edge source -> source (ooh)
            ])
    return G

def _get_random_graph(number_of_nodes, least_number_of_edges):
    """
    Generates a random graph. Probably with some cycles. This graph is not guaranteed to be connected.

    """
    G = nx.DiGraph()
    G.add_nodes_from(range(number_of_nodes))
    
    for i in range(least_number_of_edges):
        G.add_weighted_edges_from([(randint(0, number_of_nodes),
                                    randint(0, number_of_nodes), 1)])

  
    return G
              
        
# class TestGenerateBN(unittest.TestCase):
#     def test_dummy(self):
#         self.assertEqual(1,1)

if __name__ == "__main__":
    unittest.main()
    

