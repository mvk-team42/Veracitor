import networkx as nx
#import matplotlib.pyplot as plt
import tidaltrust as tt
import generate_bn as gbn
import sunny.sample_bounds as sb
from copy import copy, deepcopy

# TODO: Unittesting!

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
# The same graph as G (graf1.png) but the weights there are here under "cooking"
# and the "crime" ratings are kind of random.
# this is how you add edges to the global graph I think y'all
Gtags.add_edges_from([(1,2,dict(cooking=10, crime=4)),
                      (1,3,dict(cooking=8, crime=7)),
                      (1,4,dict(cooking=9, crime=6)),
                      (2,5,dict(cooking=9, crime=9)),
                      (3,5,dict(cooking=10, crime=5)),
                      (3,6,dict(cooking=10, crime=6)),
                      #(3,7,dict(cooking=7)),
                      (4,5,dict(cooking=8, crime=7)),
                      (4,6,dict(cooking=9, crime=6)),
                      (5,7,dict(cooking=8, crime=5)),
                      (6,7,dict(cooking=6, crime=7)),
                      (6,8,dict(cooking=5, crime=7)),
                      (8,4,dict(cooking=5, crime=7)),
                      (3,2,dict(cooking=5, crime=7)),
                      (2,1,dict(cooking=5, crime=7)),
                      ])


### TEST TIDALTRUST
#print Gtags[1]
#print Gtags[2]
#print nx.to_dict_of_dicts(Gtags)

#print "Gtags (tag=cooking): "+str(tt.compute_trust(bayesianNetwork=Gtags, source=1, sink=7, decision=None, tag="cooking"))
#print "Gtags (tag=crime): "+str(tt.compute_trust(bayesianNetwork=Gtags, source=1, sink=7, decision=None, tag="crime"))

#nx.draw(G)
#nx.draw_circular(G2)
#nx.draw_spectral(Gtags)
#nx.draw_spectral(Gtags)
#nx.draw_spectral(Gtags)


print tt.compute_trust(network=Gtags, source=1, sink=7, tag="cooking")
#print "G (ordinary weighted graph): "+str(tt.compute_trust(bayesianNetwork=G, source=1, sink=7, decision=None))


#plt.show()

### TEST GENERATEBN
Gtags2 = deepcopy(Gtags)
#Gtags2.add_edges_from([(8,4,dict(cooking=5)), (9,8,dict(cooking=5)), (10,9,dict(cooking=5)), (11,10,dict(cooking=5)), (0,1,dict(cooking=5))])
#print nx.to_dict_of_dicts(gbn.networkx_generate_bn(Gtags2, 1, 7, "cooking"))
#print nx.to_dict_of_dicts(gbn.golbeck_generate_bn(Gtags2, 1, 7, "cooking"))
#nx.draw_circular(Gtags2)
#plt.show()

print "Running sample bounds"
print sb.sample_bounds(Gtags,1,7, {}, {},'crime')

### TEST SAMPLE-BOUNDS


