import networkx as nx
import sample_bounds as sb
import sunny

G = nx.DiGraph()
G.add_edges_from([(u'mrunelov',u'dmol',dict(Trust=12)), (u'dmol', u'john',dict(Trust=4))])
sunny.sunny(G,'mrunelov','john', tag='Trust')
