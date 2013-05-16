import networkx as nx
import sample_bounds as sb
from veracitor.database import *
import sunny
from veracitor.algorithms import tidaltrust as tt

networkModel.build_network_from_db()
G = networkModel.get_global_network()
print "Tidal Trust run:"
print tt.compute_trust(G,'mrunelov','Prod1',tag='Trust')['trust']
print "Sunny run:"
print sunny.sunny(G,'mrunelov','Prod1', tag='Trust')['trust']
