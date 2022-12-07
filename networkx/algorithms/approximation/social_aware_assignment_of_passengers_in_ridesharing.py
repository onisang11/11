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

__all__ = ["match_and_merge", "find_matching"]

@not_implemented_for("directed")
def match_and_merge(G: nx.Graph,k: int) -> list:
    """
    An approximation algorithm for any k ≥ 3, provides a solution for the social aware assignment problem with a ratio of 1/(k−1).
    
    As described in the article under the section "Algorithm 1: Match and Merge".
    
    Function receives a graph G and a number k, and returns a partition P of G of all matched sets.
    
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
    # Empty implementation
    return [1]

@not_implemented_for("directed")
def find_matching(G_l: nx.Graph, l: int, Opt: list) -> list:
    """
    As described in the article under the section "Procedure 2: Find matching".

    Function receives a graph G_l, a number l which is a corresponding round index l
    And an optimal partition Opt (assuming that every S in Opt is a connected component), and returns a matching R_l in G.
    
    Finds a matching with a size of at least (|V_l'|-|O|)/(k-1) where V_l' is the set of
    All the single nodes in G_l and O is the set of all the single nodes in Opt
    That are also not matched in M1 (The maximal matching found
    In the first round of Match and Merge algorithm).

    :param G_l: Graph
    :param l: Corresponding round index
    :param Opt: Optimal partition
    :return: A matching R_l in G_l

    Example
    >>> G = nx.Graph()
    >>> list_of_edges = [(1, 2), (1, 3), (1, 5), (1, 6), (2, 4), (2, 7), (3, 4), (3, 5), (3, 6), (4, 5), (4, 6), (4, 7), (5, 8), (6, 7), (6, 8)]
    >>> G.add_edges_from(list_of_edges)
    >>> l = 3
    >>> Opt = [[1, 2, 3], [4, 5, 6], [7, 8]]
    >>> find_matching(G, l, P)
    [1, 2, 3]
    """
    # Empty implementation
    return [1]


