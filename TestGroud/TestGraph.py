# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 18:29:44 2019

@author: Sahan Ahmad
"""
import networkx as nx
import matplotlib.pyplot as plt


G = nx.DiGraph()

G.add_node("A")
G.add_node("B")
G.add_edge("A","B",weight=15)
G.add_edge("B","A",weight=10)

print(G.edges(data='weight'))

