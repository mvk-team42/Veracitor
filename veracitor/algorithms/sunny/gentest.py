import networkx as nx
import sample_bounds as sb
import sunny

G = nx.DiGraph()
G.add_edges_from([(u'mrunelov',u'dmol',dict(cooking=12))])
sunny.sunny(G,'mrunelov','dmol')
