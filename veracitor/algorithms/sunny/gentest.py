import networkx as nx
import sample_bounds as sb
from veracitor.database import *
import sunny
from veracitor.algorithms import tidaltrust as tt

networkModel.build_network_from_db()
G = networkModel.get_global_network()
print "Tidal Trust run:"
print tt.compute_trust(G,'mrunelov','john',tag='Trust')
print "Sunny run:"
print sunny.sunny(G,u'mrunelov',u'john', tag='Trust')
