import unittest
import networkx as nx
import tidaltrust as tt
from copy import copy, deepcopy

class TestTidalTrust(unittest.TestCase):
    def test_parameters_constant(self):
        """
        Input parameter objects are not changed by compute_trust

        """
        
        # Test for weighted graph
        G = self._get_weighted_graph()
        source = 1
        sink = 7
        Gcopy = deepcopy(G)
        tt.compute_trust(G, source, sink)
        self.assertEqual(nx.to_dict_of_dicts(Gcopy),
                         nx.to_dict_of_dicts(G))
        self.assertEqual(7, sink)
        self.assertEqual(1, source)

        # Test for tagrated graph
        G = self._get_tagrated_graph()
        Gcopy = deepcopy(G)
        tt.compute_trust(G, source, sink, tag="cooking")
        self.assertEqual(nx.to_dict_of_dicts(Gcopy),
                         nx.to_dict_of_dicts(G))
        self.assertEqual(7, sink)
        self.assertEqual(1, source)

        # Test with decision array
        tt.compute_trust(G, source, sink, tag="cooking", decision=[5])
        self.assertEqual(nx.to_dict_of_dicts(Gcopy),
                         nx.to_dict_of_dicts(G))
        self.assertEqual(7, sink)
        self.assertEqual(1, source)

    def test_returns_none_when_no_paths(self):
        """
        compute_trust returns None when no trust value could be found
        """
        G = nx.DiGraph()
        G.add_nodes_from([1,2]) 
       
        # Test when there really is no path to begin with (no edges)
        self.assertIsNone(tt.compute_trust(G,1,2))

        # Test when edges have the wrong tag
        G.add_edge(1,2,dict(cooking=4))
        self.assertIsNone(tt.compute_trust(G,1,2,tag="crime"))
        
        # Test when input nodes are not in the graph
        self.assertIsNone(tt.compute_trust(G,1,5,tag="crime"))
        self.assertIsNone(tt.compute_trust(G,7,2,tag="crime"))
        self.assertIsNone(tt.compute_trust(G,10,11,tag="crime"))

    def test_raises_exceptions_on_strange_input(self):
        """
        Raises exceptions when input was objects of the wrong type

        """
        G = self._get_tagrated_graph()

        # Test for None source/sink
        self.assertRaises(TypeError, tt.compute_trust, G, None, 7)
        self.assertRaises(TypeError, tt.compute_trust, G, 1, None)
        self.assertRaises(TypeError, tt.compute_trust, G, None, None)

        # Test for None graph
        self.assertRaises(TypeError, tt.compute_trust, None, 1, 7)
        
        # Test for when decision is not a an iterable
        self.assertRaises(TypeError, tt.compute_trust, G, 1, 7, decision=unittest.TestCase)        
        
        # Test for bayesianNetwork is not a graph
        self.assertRaises(Exception, tt.compute_trust, "string", 1, 7)

        
        


    ### HELP METHODS
    def _get_weighted_graph(self):
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

    def _get_tagrated_graph(self):
        Gtags = nx.DiGraph()
        Gtags.add_edges_from([(1,2,dict(cooking=10, crime=4)),
                              (1,3,dict(cooking=8, crime=7)),
                              (1,4,dict(cooking=9, crime=6)),
                              (2,5,dict(cooking=9, crime=9)),
                              (3,5,dict(cooking=10, crime=5)),
                              (3,6,dict(cooking=10, crime=6)),
                              (4,5,dict(cooking=8, crime=7)),
                              (4,6,dict(cooking=9, crime=6)),
                              (5,7,dict(cooking=8, crime=5)),
                              (6,7,dict(cooking=6, crime=7)),
                              ])
        return Gtags

# class TestGenerateBN(unittest.TestCase):
#     def test_dummy(self):
#         self.assertEqual(1,1)

if __name__ == "__main__":
    unittest.main()
    

