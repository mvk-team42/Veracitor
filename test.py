import networkx as nx
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

print G.nodes()
print G.edges()
print G[1][2]['weight']
print nx.to_dict_of_dicts(G)

#nx.draw(G)
#nx.draw_circular(G)
#nx.draw_spectral(G)

shortest = nx.all_shortest_paths(G, source=1, target=7)
print shortest
print dir(shortest)
plt.show()
