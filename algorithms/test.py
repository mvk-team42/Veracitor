import networkx as nx
import matplotlib.pyplot as plt
from tidaltrust import TidalTrust as tt

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

G2 = nx.DiGraph()

G2.add_weighted_edges_from([(1,2,5),
                            (1,3,4),
                            (2,4,10),
                            (2,5,10),
                            (3,6,9),
                            (4,7,2),
                            (5,8,8),
                            (6,8,3),
                            (8,9,7),
                            (6,7,5),
                            ])

Gtags = nx.DiGraph()

Gtags.add_edges_from([(1,2,{"ratings":dict(cooking = 4, crime = 10)})])
Gtags.add_weighted_edges_from([(2,1,5)])


print Gtags[1]
print Gtags[2]


#nx.draw(G)
#nx.draw_circular(G2)
#nx.draw_spectral(Gtags)

#print tt.tidal_trust(graph=G, source=1, sink=7)

#print tt.compute_trust(bayesianNetwork=G2, source=1, sink=9, decision=None)


plt.show()
