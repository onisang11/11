"""
===============
Degree Sequence
===============

Random graph from given degree sequence.
"""
import matplotlib.pyplot as plt
from networkx import nx

z = [5, 3, 3, 3, 3, 2, 2, 2, 1, 1, 1]
print(nx.is_graphical(z))

print("Configuration model")
G = nx.configuration_model(z, seed=23)  # configuration model, seed for reproduciblity
degree_sequence = [d for n, d in G.degree()]  # degree sequence
print(f"Degree sequence {degree_sequence}")
print("Degree histogram")
hist = {}
for d in degree_sequence:
    if d in hist:
        hist[d] += 1
    else:
        hist[d] = 1
print("degree #nodes")
for d in hist:
    print(f"{d:4} {hist[d]:6}")

pos = nx.spring_layout(G, seed=668273)  # Seed layout for reproducibility
nx.draw(G, pos=pos)
plt.show()
