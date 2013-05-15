import networkx as nx
import sample_bounds as sb
from veracitor.database import *
import sunny

networkModel.build_network_from_db()
G = networkModel.get_global_network()
print sunny.sunny(G,u'mrunelov',u'dmol', tag='Trust')
