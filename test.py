import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

G.add_edge(1,2)
G.add_edges_from([(2,1),(1,3),(3,4),(5,4),(3,2)])

print G.nodes()
print G.edges()

nx.draw(G)
plt.show()
