# -*- coding: utf-8 -*-
#    Copyright (C) 2004-2019 by
#    Aric Hagberg <hagberg@lanl.gov>
#    Dan Schult <dschult@colgate.edu>
#    Pieter Swart <swart@lanl.gov>
#    All rights reserved.
#    BSD license.
#
# Authors: Haakon H. Rød (haakonhr@gmail.com)
"""
Algorithms for asteroidal triples and asteroidal numbers in graphs.

An asteroidal triple in a graph G is a set of three non-adjacent vertices
u, v and w such that there exist a path between any two of them avoiding the
neighborhood of the third. More formally, v_j, v_k belongs to the same
connected component of G - N[v_i]. A graph which contains no asteroidal
triples is called an AT-free graph. AT-free graphs is a graph class
for which many NP-complete problems are solvable in polynomial time.
Amongst them, independent set and coloring.
"""
import networkx as nx
from networkx.utils import not_implemented_for

__all__ = ["is_at_free"]


@not_implemented_for("directed")
@not_implemented_for("multigraph")
def find_asteroidal_triple(G):

    An asteroidal triple is a triple of non-adjacent vertices such that
    there exists a path between any two of them which avoids the closed
    neighborhood of the third. It checks all independent triples of vertices
    and whether they are an asteroidal triple or not. This is done with the
    help of a data structure called a component structure.
    The component structure encodes information about which vertices belongs to
    the same connected component when the closed neighborhood of a given vertex
    is removed from the graph. The algorithm used to check is the trivial
    one, outlined in [1]_, which has a runtime of
    :math:`O(|V||\overline{E} + |V||E|)`, where the second term is the
    creation of the component structure.

    Parameters
    ----------
    G : NetworkX Graph
        The graph to check whether is AT-free or not

    certificate : bool (default: False)
        If the first detected asteroidal triple should be output, if one
        exists, or None, in the case where a graph is AT-free.

    Returns
    -------
    bool (default)
        The returned value depends on the certificate parameter. The default
        option is a bool which is True if the graph is AT-free, i.e. the
        given graph contains no asteroidal triples, and False otherwise, i.e.
        if the graph contains at least one asteroidal triple.

    tuple
        If the optional parameter `certificate` is set to True then a
        tuple containing False and an asteroidal triple, represented as a tuple
        of vertices, is returend if the graph is not AT-free. If the graph
        is AT-free a tuple with True and None is returned.

    Examples
    --------
    >>> G = nx.Graph([(0, 1), (0, 2), (1, 2), (1, 3), (1, 4), (4, 5)])
    >>> nx.is_at_free(G)
    True

    >>> G = nx.cycle_graph(6)
    >>> nx.is_at_free(G)
    False

    Notes
    -----
    The component structure and the algorithm is described in [1]_. The current
    implementation implements the trivial algorithm for simple graphs.

    References
    ----------
    .. [1] Ekkehard Köhler,
       "Recognizing Graphs without asteroidal triples",
       Journal of Discrete Algorithms 2, pages 439-452, 2004.
       https://www.sciencedirect.com/science/article/pii/S157086670400019X
    """
    def _is_asteroidal_triple(u, v, w, component_structure):
        """Check whether a triple of vertices is an asteroidal triple."""
        return (component_structure[u][v] == component_structure[u][w] and
                component_structure[v][u] == component_structure[v][w] and
                component_structure[w][u] == component_structure[w][v])

    V = set(G.nodes)

    if len(V) < 6:
        # An asteroidal triple cannot exist in a graph with 5 or less vertices.
        return None

    component_structure = create_component_structure(G)
    E_complement = set(nx.complement(G).edges)

    for e in E_complement:
        u = e[0]
        v = e[1]
        u_neighborhood = set(G[u]).union([u])
        v_neighborhood = set(G[v]).union([v])
        union_of_neighborhoods = u_neighborhood.union(v_neighborhood)
        for w in V - union_of_neighborhoods:
            if _is_asteroidal_triple(u, v, w, component_structure):
                if certificate:
                    return (False,  (u, v, w))
                else:
                    return False

    if certificate:
        return (True, None)
                return [u, v, w]

    return None


@not_implemented_for("directed")
@not_implemented_for("multigraph")
def is_at_free(G):
    """Check if a graph is AT-free.

    The method uses the `find_asteroidal_triple` method to recognize
    an AT-free graph. If no asteroidal triple is found the graph is
    AT-free and True is returned. If at least one asteroidal triple is
    found the graph is not AT-free and False is returned.

    Parameters
    ----------
    G : NetworkX Graph
        The graph to check whether is AT-free or not.

    Returns
    -------
    bool
        True if G is AT-free and False otherwise.

    Examples
    --------
    >>> G = nx.Graph([(0, 1), (0, 2), (1, 2), (1, 3), (1, 4), (4, 5)])
    >>> nx.is_at_free(G)
    True

    >>> G = nx.cycle_graph(6)
    >>> nx.is_at_free(G)
    False
    """
    asteroidal_triple = find_asteroidal_triple(G)
    if asteroidal_triple:
        return False
    else:
        return True


@not_implemented_for("directed")
@not_implemented_for("multigraph")
def create_component_structure(G):
    r"""Create component structure for G.

    A *component structure* is an `nxn` array, denoted `c`, where `n` is
    the number of vertices,  where each row and column corresponds to a vertex.

    .. math::
        c_{uv} = \begin{cases} 0, if v \in N[u] \\
            k, if v \in component k of G \setminus N[u] \end{cases}

    Where `k` is an arbitrary label for each component. The structure is used
    to simplify the detection of asteroidal triples.

    Parameters
    ----------
    G : NetworkX Graph
        Undirected, simple graph.

    Returns
    -------
    component_structure : dictionary
        A dictionary of dictionaries, keyed by pairs of vertices.

    """
    V = set(G.nodes)
    component_structure = {}
    for v in V:
        label = 0
        closed_neighborhood = set(G[v]).union(set([v]))
        row_dict = {}
        for u in closed_neighborhood:
            row_dict[u] = 0

        G_reduced = G.subgraph(set(G.nodes) - closed_neighborhood)
        for cc in nx.connected_components(G_reduced):
            label += 1
            for u in cc:
                row_dict[u] = label

        component_structure[v] = row_dict

    return component_structure
