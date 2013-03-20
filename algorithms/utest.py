import unittest
import networkx as nx
import tidaltrust as tt
import generate_bn as gbn
from copy import copy, deepcopy

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



class TestGenerateBN(unittest.TestCase):
    """
    Tests the module generate_bn    
        
    """
    def test_cycle_removal(self):
        """
        (generate_bn) Removes cycles from graphs
        
        """
        G = _get_graph_with_cycles()
        loops = nx.simple_cycles(G)
        self.assertNotEqual(loops, [])
        G = gbn.golbeck_generate_bn(G, 1, 7)
        loops = nx.simple_cycles(G)
        self.assertEqual(loops, [])
        


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
        
# class TestGenerateBN(unittest.TestCase):
#     def test_dummy(self):
#         self.assertEqual(1,1)

if __name__ == "__main__":
    unittest.main()
    

