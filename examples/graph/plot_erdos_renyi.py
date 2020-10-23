"""
===========
Erdos Renyi
===========

Create an G{n,m} random graph with n nodes and m edges
and report some properties.

This graph is sometimes called the Erdős-Rényi graph
but is different from G{n,p} or binomial_graph which is also
sometimes called the Erdős-Rényi graph.
"""

import matplotlib.pyplot as plt
from networkx import nx

n = 10  # 10 nodes
m = 20  # 20 edges

# Use seed for reproducibility
G = nx.gnm_random_graph(n, m, seed=20160)

# some properties
print("node degree clustering")
for v in nx.nodes(G):
    print(f"{v} {nx.degree(G, v)} {nx.clustering(G, v)}")

print()
print("the adjacency list")
for line in nx.generate_adjlist(G):
    print(line)

pos = nx.spring_layout(G, seed=6720)  # Seed for reproducible layout
nx.draw(G, pos=pos)
plt.show()
