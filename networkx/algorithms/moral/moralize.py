# -*- coding: utf-8 -*-
#   Copyright (C) 2011-2018 by
#   Julien Klaus <julien.klaus@uni-jena.de>
#   All rights reserved.
#   BSD license.
#   Copyright 2016-2018 NetworkX developers.
#   NetworkX is distributed under a BSD license
#
# Authors: Julien Klaus <julien.klaus@uni-jena.de>
"""Function for computing the moral graph of a directed graph."""

import networkx as nx
from networkx.utils import not_implemented_for
import itertools
# TODO: remove matplotlib later
import matplotlib.pyplot as plt


@not_implemented_for('undirected')
def get_moral_graph(G):
    r"""Return the Moral Graph

        Returns the moralized graph of a given directed graph.

        Parameters
        ----------
        G : NetworkX graph
            Directed graph

        Returns
        -------
        H : NetworkX graph
            The undirected moralized graph of G

        Notes
        ------
        A moral graph is an undirected graph H = (V, E) generated from a
        directed Graph, where if a node has more than one parent node, edges
        between these parent nodes are inserted and all directed edges become
        undirected.

        https://en.wikipedia.org/wiki/Moral_graph

        References
        ----------
        .. [1] Wray L. Buntine. 1995. Chain graphs for learning.
               In Proceedings of the Eleventh conference on Uncertainty
               in artificial intelligence (UAI'95)
    """
    if G is None:
        raise ValueError("Expected NetworkX graph!")

    H = G.copy()
    for node in H.nodes():
        predecessors = list(H.predecessors(node))
        # connect the parents of a given node
        if len(predecessors) > 1:
            # r is the number of elements per combination
            predecessors_combinations = itertools.combinations(predecessors, r=2)
            H.add_edges_from(predecessors_combinations)
    # remove the direction of edges
    return H.to_undirected()


if __name__ == "__main__":
    graph = nx.DiGraph()
    graph.add_nodes_from([1, 2, 3, 4, 5, 6, 7])
    graph.add_edges_from([(1, 2), (3, 2), (4, 1), (4, 5), (6, 5), (7, 5)])
    plt.subplot(121)
    nx.draw_networkx(graph, with_labels=True)

    moralize = get_moral_graph(graph)
    plt.subplot(122)
    nx.draw_networkx(moralize, with_labels=True)
    plt.show()
