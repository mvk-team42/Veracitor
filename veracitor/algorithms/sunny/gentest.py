import networkx as nx
import sample_bounds as sb

G = nx.DiGraph()
G.add_edges_from([(u'1',u'2',dict(cooking=12))])
print sb.sample_bounds(G,'1','2',100)
