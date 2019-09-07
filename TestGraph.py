# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 18:29:44 2019

@author: Sahan Ahmad
"""
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
G.add_node(1)
G.add_nodes_from([2, 3])
H = nx.path_graph(10)
G.add_nodes_from(H)
G.add_edge(1, 2)
e = (2, 3)
G.add_edge(*e)
G.add_edges_from(H.edges)
print(list(G.nodes))
print(list(G.edges))
# Drawing A Graph
G = nx.petersen_graph()
plt.subplot(121)

nx.draw(G, with_labels=True, font_weight='bold')
plt.subplot(122)

nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
