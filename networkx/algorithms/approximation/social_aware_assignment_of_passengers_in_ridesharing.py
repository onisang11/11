"""
Implementation of the Social Aware Assignment of Passengers in Ridesharing
Which was described in the article:
Levinger, C., Hazon, N., & Azaria, A. (2022). Social Aware Assignment of Passengers in Ridesharing.
In Proceedings of the 2022 ACM Conference on Economics and Computation (EC 2022).
Short version: http://azariaa.com/Content/Publications/Social_Assignment_SA.pdf
Full version: https://github.com/VictoKu1/ResearchAlgorithmsCourse1/blob/main/Article/2022%2C%20Chaya%20Amos%20Noam%2C%20Socially%20aware%20assignment%20of%20passengers%20in%20ride%20sharing.pdf
Paper ID: 1862

Implementation of match_and_merge
algorithm is based on the pseudocode from the article
which is written by Victor Kushnir. 
"""
import networkx as nx
from networkx.utils import not_implemented_for
from itertools import chain
__all__ = ["match_and_merge"]
@not_implemented_for("directed")
def match_and_merge(G: nx.Graph, k: int) -> list:
    """
    An approximation algorithm for any k ≥ 3, provides a solution for the social aware assignment problem with a ratio of 1/(k-1).

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
        # Implement G_l=(V_l,E_l) using a dictionary which contains a tuple of V_l and E_l
        G = {1: G}
        # Should contain the maximal matching of G_l
        M = {}
        #Loop to find the lth maximal matching and put it in G_(l+1)
        for l in range(1, k-1):
            # Initialization of the unified nodes list
            unified_nodes=[]
            # Find the maximal matching of G_l
            M[l] = list(nx.maximal_matching(G[l]))
            # Make sure that G_(l+1) is a empty graph (It was one of the steps of the algorithm in the article)
            G[l+1] = nx.Graph()
            # Put the nodes of G_l in G_(l+1)
            G[l+1].add_nodes_from(G[l].nodes())
            # For every match in M_l, add a unified node to G_(l+1) so it will be used to find it when needed
            for match in M[l]:
                # Arrange the match, so if there is tuple in a tuple, it will be on the same level.
                match = tuple(sorted(match, key=lambda x: (isinstance(x, tuple), x)))
                # Add the match to the unified nodes dictionary, so it will be easier to find the unified nodes in each round
                unified_nodes.extend(match)
                # Add a unified node to G_(l+1), which is a tuple of the nodes in the match
                G[l+1].add_node(match)
                # Remove the nodes in the match from G_(l+1)
                G[l+1].remove_nodes_from(list(match))
            # For every unified node in G_(l+1), add every v_q in G_(l+1) that is connected to it in G_l, add an edge between them in G_(l+1)
            for unified_node in G[l+1].nodes():
                for v_q in G[l+1].nodes():
                    if G[l].has_edge(unified_node, v_q):
                        G[l+1].add_edge(unified_node, v_q)
                    # If v_q is a tuple, check if it contains a node that is connected to the unified node in G_l
                    elif isinstance(v_q, tuple):
                        for node in v_q:
                            if G[l].has_edge(unified_node, node):
                                G[l+1].add_edge(unified_node, v_q)
                                break
        # Initialization of the partition P and for every unified node (which is a tuple of nodes) in G_(k-1), add it to P
        P = [list(unified_node) for unified_node in G[k-1].nodes()]
        # Return P
        return P