"""
Implementation of the Social Aware Assignment of Passengers in Ridesharing
Which was described in the article:
Levinger, C., Hazon, N., & Azaria, A. (2022). Social Aware Assignment of Passengers in Ridesharing.
In Proceedings of the 2022 ACM Conference on Economics and Computation (EC 2022).
Short version: http://azariaa.com/Content/Publications/Social_Assignment_SA.pdf
Full version: https://github.com/VictoKu1/ResearchAlgorithmsCourse1/blob/main/Article/2022%2C%20Chaya%20Amos%20Noam%2C%20Socially%20aware%20assignment%20of%20passengers%20in%20ride%20sharing.pdf
Paper ID: 1862

Implementation of match_and_merge and find_matching
Functions are based on the pseudocode from the article which are
Written by Victor Kushnir. 
"""

import networkx as nx
from networkx.utils import not_implemented_for

__all__ = ["match_and_merge"]


@not_implemented_for("directed")
def match_and_merge(G: nx.Graph, k: int) -> list:
    """
    An approximation algorithm for any k ≥ 3, provides a solution for the social aware assignment problem with a ratio of 1/(k−1).

    As described in the article under the section "Algorithm 1: Match and Merge".

    Function receives a graph G and a number k, and returns a partition P of G of all matched sets.

    The algorithm consists of k - 1 rounds. Each round is composed of a matching phase followed by a merging phase.
    Specifically, in round l MnM computes a maximum matching, M_l ⊆ E_l , for G_l (where G_1 = G). In the merging phase, MnM creates a graph
    G_(l+1) that includes a unified node for each pair of matched nodes. G_(l+1) also includes all unmatched nodes, along with their
    edges to the unified nodes. Clearly, each node in V_l is composed of up-to l nodes
    from V_1. Finally, MnM returns the partition, P, of all the matched sets.

    :param G: Graph
    :param k: Number of passengers
    :return: A partition P of G of all matched sets

    Example where G={(v1,v2),(v2,v3),(v3,v4),(v4,v5),(v4,v6)} and k=4:
    >>> G = nx.Graph()
    >>> list_of_edges = [(1, 2), (2, 3), (3, 4), (4, 5), (4, 6)]
    >>> G.add_edges_from(list_of_edges)
    >>> k = 4
    >>> match_and_merge(G, k)
    [[1, 2], [3, 4, 5, 6]]
    """

    # Check if k is correct
    if k < 3:
        # If k is negative, raise an error
        if k < 0:
            raise nx.NetworkXError("k should be 0≤k≤|V(G)|")

        # If k is 0, return an empty list
        elif k == 0:
            return []

        # If k is 1, return a partition of G where each node is a list
        elif k == 1:
            return [[node] for node in G.nodes()]

        # If k is 2, run the maximum matching algorithm on G and return the result
        else:
            return list(nx.maximal_matching(G))

    else:
        # Implement G_l=(V_l,E_l) using a list which contains a tuple of V_l and E_l
        G_l = [(G.nodes(), G.edges())]

        for l in range(1, k-1):

            # Put maximum matching of G_l in M_l
            M_l = nx.maximal_matching(nx.Graph(G_l[l-1][1]))

            # Put an empty graph in G_(l+1)
            G_l.append(([], []))

            # Put V_l in V_(l+1)
            G_l[l+1][0] = G_l[l][0]

            # TODO: For every (v_{i_1,i_2,i_3,i_4,.....,i_l},v_j) in M_l, merge it to v_{i_1,i_2,i_3,i_4,.....,i_l,j}, put it in V_(l+1) and remove v_{i_1,i_2,i_3,i_4,.....,i_l} and v_j from V_(l+1)

            # TODO: For every v_{i_1,i_2,i_3,i_4,.....,i_(l+1)} in V_(l+1) and v_q in V_(l+1), check if (v_{i_1,i_2,i_3,i_4,.....,i_(l+1)},v_q) in E_l, if so, put it in E_(l+1)

            # Initialization of the partition list
            P = []

            # TODO: For every v_{i_1,i_2,i_3,i_4,.....,i_j} in G_l[k][0], add v_{i_1,i_2,i_3,i_4,.....,i_j} to P

            # Return P
            return P






















