""" Provides a function for computing the extendability of a
graph which is undirected, simple, connected and bipartite. """


import networkx as nx
from networkx.utils import not_implemented_for


__all__ = [
    "find_extendability",
]


@not_implemented_for("directed")
@not_implemented_for("multigraph")
def find_extendability(G):
    """Computes the extendability of a graph.

    Definition
    Graph G is $k$-extendable if and only if G has a perfect matching and every
    set of $k$ independent edges can extend to perfect matching.

    EXTENDABILITY PROBLEM
    Input: A graph G and a positive integer $k$.
    Output: Is G $k$-extendable?

    In general case the above problem is co-NP-complete([2]).
    If graph G is bipartite, then it can be decided in polynomial time([1]).

    The maximization version of the EXTENDABILITY PROBLEM asks to compute the
    maximum $k$ for which G is $k$-extendable.

    Let G be a simple, connected, undirected and bipartite graph with a perfect
    matching M and bipartition (U,V). The residual graph of G, denoted by $G_M$,
    is the graph obtained from G by directing the edges of M from V to U and the
    edges that do not belong to M from U to V.

    Lemma([1])
    Let M be a perfect matching of G. G is k-extendable if and only if its residual
    graph $G_M$ is strongly connected and there are $k$ vertex-disjoint directed
    paths between every vertex of U and every vertex of V.

    Parameters
    ----------

        G : NetworkX Graph

    Returns
    -------

        extendability: int

    Raises
    ------

        NetworkXError
           If the graph G is not simple.
           If the graph G is disconnected.
           If the graph G is not bipartite.
           If the graph G does not contain a perfect matching.
           If the residual graph of G is not strongly connected.

    Notes
    -----

        Time complexity O($n^3$ $m^2$)) where $n$ is the number of vertices
        and $m$ is the number of edges.

    References
    ----------

        ..[1] "A polynomial algorithm for the extendability problem in bipartite graphs",
              J. Lakhal, L. Litzler, Information Processing Letters, 1998.
        ..[2] "The matching extension problem in general graphs is co-NP-complete",
              Jan Hackfeld, Arie M. C. A. Koster, Springer Nature, 2018.

    """

    for edge in G.edges:
        if edge[0] == edge[1]:
            raise nx.NetworkXError("Graph G is not simple")

    if not nx.is_connected(G):
        raise nx.NetworkXError("Graph G is not connected")

    if not nx.bipartite.is_bipartite(G):
        raise nx.NetworkXError("Graph G is not bipartite")

    U, V = nx.bipartite.sets(G)

    # Variable $k$ stands for the extendability of graph G
    k = float("Inf")

    # Find a maximum matching M
    maximum_matching = nx.bipartite.hopcroft_karp_matching(G)

    if nx.is_perfect_matching(G, maximum_matching):

        # Construct a list consists of the edges of M by directing them from V to U
        perfect_matching = []
        for vertex in maximum_matching.keys():
            if vertex in V:
                neighbor = maximum_matching[vertex]
                perfect_matching.append((vertex, neighbor))

        # Direct all the edges of G
        directed_edges = []
        for edge in G.edges:
            first_coordinate, second_coordinate = edge[0], edge[1]
            reverse_pair = (second_coordinate, first_coordinate)
            if first_coordinate in U and second_coordinate in V:
                if reverse_pair in perfect_matching:
                    directed_edges.append(reverse_pair)
                else:
                    directed_edges.append(edge)
            if first_coordinate in V and second_coordinate in U:
                if edge in perfect_matching:
                    directed_edges.append(edge)
                else:
                    directed_edges.append(reverse_pair)

        # Construct the residual graph of G
        residual_G = nx.DiGraph()
        residual_G.add_nodes_from(G.nodes)
        residual_G.add_edges_from(directed_edges)

        if nx.is_strongly_connected(residual_G):

            # Find the number of maximum disjoint paths between every vertex of U and V and keep the minimum
            for u in U:
                for v in V:
                    vertex_disjoint_paths = []
                    paths = nx.node_disjoint_paths(residual_G, u, v)
                    for path in paths:
                        vertex_disjoint_paths.append(path)
                    k = min(k, len(vertex_disjoint_paths))
        else:
            raise nx.NetworkXError("The residual graph of G is not strongly connected")
    else:
        raise nx.NetworkXError("Graph G does not contain a perfect matching")
    return k
