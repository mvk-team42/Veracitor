import networkx as nx
import sample_bounds as sb
import sunny

G = nx.DiGraph()
G.add_edges_from([(u'mrunelov',u'alfred',dict(cooking=12))])
sunny.sunny(G,'mrunelov','alfred')
