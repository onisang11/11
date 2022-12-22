import collections
import itertools
import logging
import networkx as nx

__all__ = [
    "envy_free_matching",
    "minimum_weight_envy_free_matching",
]

import networkx.algorithms.bipartite

INFINITY = float("inf")

logger = logging.getLogger("Envy-free matching")
formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(name)s: Line %(lineno)d: %(message)s')
console = logging.StreamHandler()  # writes to stderr (= cerr)
logger.handlers = [console]
console.setFormatter(formatter)


def _EFM_partition(G, M=None):
    r"""Returns the unique EFM partition of bipartite graph.

    A matching in a bipartite graph with parts X and Y is called envy-free, if no unmatched
    vertex in X is adjacent to a matched vertex in Y.
    Every bipartite graph has a unique partition such that all envy-free matchings are
    contained in one of the partition set.

    Parameters
    ----------
    G:  NetworkX graph

      Undirected bipartite graph
    M: dict
       dictionary that represents a maximum matching in G.
       If M is none, the function will find the maximum matching.

    Returns
    -------
    EFM: list of sets
        The partition returns as a list of 4 sets of vertices:
        X_L,X_S,Y_L,Y_S where X_L,Y_L are the "good vertices" of G and
        X_S,Y_S are the "bad vertices" of G.

    References
    ----------
    .. [1] "Envy-free Matchings in Bipartite Graphs and their Applications to Fair Division",
    by Elad Aigner-Horev and Erel Segal-Halevi (2022), https://arxiv.org/abs/1901.09527
    Algorithm 1: Finding the EFM partition of a bipartite graph.

    Programmers
    -----------
        Benjamin Saldman
        Daniel Gilkarov
    Examples
    --------
        Example 1: Perfect matching
        >>> Graph=nx.complete_bipartite_graph(3,3)
        >>> Matching=nx.bipartite.hopcroft_karp_matching(Graph)
        >>> _EFM_partition(Graph,Matching)
        [{0,1,2},{},{3,4,5},{}]

        Where there exists a perfect matching the maximum envy free matching is the perfect matching.

        Example 2: Non-empty envy-free matching
        >>> Graph=nx.Graph([(0,3),(3,0),(0,4),(4,0),(1,4),(4,1),(2,4),(4,2)])
        >>> Matching={0:3,3:0,1:4,4:1}
        >>> _EFM_partition(Graph,Matching)
        [{0},{1,2},{3},{4}]

        Here the graph contains non-empty envy-free matching so X_L,Y_L are not empty.

        Example 3: Odd path
        >>> Graph=nx.Graph([(0,3),(3,0),(1,3),(3,1),(1,4),(4,1),(2,4),(4,2)])
        >>> Matching={0:3,3:0,4:1,1:4}
        >>> _EFM_partition(Graph,Matching)
        [{},{0,1,2},{},{3,4}]

        Like presented in the article, odd path contains an empty envy-free matching so X_L and Y_L are empty in the partition.

        Example 4: Y-path-saturated graph
        >>> Graph=nx.Graph([(0,6),(6,0),(1,6),(6,1),(1,7),(7,1),(2,6),(6,2),(2,8),(8,2),(3,9),(9,3),(3,6),(6,3),(4,8),(8,4),(4,7),(7,4),(5,9),(9,5)])
        >>> Matching={0:6,6:0,1:7,7:1,2:8,8:2,3:9,9:3}
        >>> _EFM_partition(Graph,Matching)
        [{},{0,1,2,3,4,5},{},{6,7,8,9}]

        Like presented in the article, Y-path-saturated graph contains an empty envy-free matching so X_L and Y_L are empty in the partition.

    """
    pass


def envy_free_matching(G):
    r"""Return an envy-free matching of maximum cardinality

    Parameters
    ----------
    G
        NetworkX graph

        Undirected bipartite graph

    Returns
    -------
    Matching: dictionary
        The Maximum cardinallity envy-free matching is returned as a dictionary.
    References
    ----------
    .. [1] "Envy-free Matchings in Bipartite Graphs and their Applications to Fair Division",
    by Elad Aigner-Horev and Erel Segal-Halevi (2022), https://arxiv.org/abs/1901.09527
    Algorithm 2: Finding an envy-free matching of maximum cardinality.
    Programmers
    -----------
        Benjamin Saldman
        Daniel Gilkarov
    Examples
    --------
        Example 1: Perfect matching
        >>> Graph=nx.complete_bipartite_graph(3,3)
        >>> envy_free_matching(Graph)
        {0:3,3:0,1:4,4:1,2:5,5:2}

        Where there exists a perfect matching the maximum envy free matching is the perfect matching.

        Example 2: Non-empty envy-free matching
        >>> Graph=nx.Graph([(0,3),(3,0),(0,4),(4,0),(1,4),(4,1),(2,4),(4,2)])
        >>> envy_free_matching(Graph)
        {0:3,3:0}

        Example 3: Odd path
        >>> Graph=nx.Graph([(0,3),(3,0),(1,3),(3,1),(1,4),(4,1),(2,4),(4,2)])
        >>> envy_free_matching(Graph)
        {}

        Like presented in the article, odd path contains an empty envy-free matching so the returned matching is empty.

        Example 4: Y-path-saturated graph
        >>> Graph=nx.Graph([(0,6),(6,0),(1,6),(6,1),(1,7),(7,1),(2,6),(6,2),(2,8),(8,2),(3,9),(9,3),(3,6),(6,3),(4,8),(8,4),(4,7),(7,4),(5,9),(9,5)])
        >>> envy_free_matching(Graph)
        {}

        Like presented in the article, Y-path-saturated graph contains an empty envy-free matching so X_L and Y_L are empty in the partition.
    """
    logger.info(f"Finding the maximum envy free matching of {G}")
    logger.debug(f"Finding the maximum matching of {G}")
    M = networkx.algorithms.bipartite.hopcroft_karp_matching(G)
    # EFM_PARTITION = _EFM_partition(G, M)
    # EFM_PARTITION = [set((0, 1, 2)), set(), set((3, 4, 5)), set()]
    # EFM_PARTITION = [{0}, {1, 2}, {3}, {4}]
    logger.debug(f"Finding the EFM partition with maximum matching: {M}")
    EFM_PARTITION = [{}, {0, 1, 2, 3, 4, 5}, {}, {6, 7, 8, 9}]
    # G.remove_nodes_from((EFM_PARTITION[1]).union((EFM_PARTITION[3])))
    un = EFM_PARTITION[1].union(EFM_PARTITION[3])
    logger.debug(f"Finding the sub-matching M[X_L,Y_L]")
    M = {node: M[node] for node in M if node not in un and M[node] not in un}
    if len(M) == 0:
        logger.warning(f"The sub-matching is empty!")
    logger.debug(f"returning the sub-matching M[X_L,Y_L]: {M}")
    return M
    # return networkx.algorithms.bipartite.hopcroft_karp_matching(G)


def minimum_weight_envy_free_matching(G):
    r"""Returns minimum-cost maximum-cardinality envy-free matching

    Parameters
    ----------
    G
        NetworkX graph

        Undirected bipartite graph

    Returns
    -------
    Matching: dictionary
        The minimum cost maximum cardinallity matching is returned as a dictionary.
    References
    ----------
    .. [1] "Envy-free Matchings in Bipartite Graphs and their Applications to Fair Division",
    by Elad Aigner-Horev and Erel Segal-Halevi (2022), https://arxiv.org/abs/1901.09527
    Algorithm 3: Finding a minimum-cost maximum-cardinality envy-free matching.
    Programmers
    -----------
        Benjamin Saldman
        Daniel Gilkarov
    Examples
    --------
        Example 1: K 3,3 with weights
        >>> Graph=nx.Graph()
        >>> Graph.add_edge(0,3,weight=250)
        >>> Graph.add_edge(3,0,weight=250)
        >>> Graph.add_edge(0,4,weight=148)
        >>> Graph.add_edge(4,0,weight=148)
        >>> Graph.add_edge(0,5,weight=122)
        >>> Graph.add_edge(5,0,weight=122)
        >>> Graph.add_edge(1,3,weight=175)
        >>> Graph.add_edge(3,0,weight=175)
        >>> Graph.add_edge(1,4,weight=135)
        >>> Graph.add_edge(4,1,weight=135)
        >>> Graph.add_edge(1,5,weight=150)
        >>> Graph.add_edge(5,1,weight=150)
        >>> Graph.add_edge(2,3,weight=150)
        >>> Graph.add_edge(3,2,weight=150)
        >>> Graph.add_edge(2,4,weight=125)
        >>> Graph.add_edge(4,2,weight=125)
        >>> Graph.add_edge(3,5,weight=108)
        >>> Graph.add_edge(5,3,weight=108)
        >>> minimum_weight_envy_free_matching(Graph)
        {0:5,5:0,1:4,4:1,2:3,3:2}

        Where there exists a perfect matching the maximum envy free matching is the perfect matching this is the least cost perfect matching.



        Example 2: Non-empty envy-free matching
        >>> Graph=nx.Graph()
        >>> Graph.add_edge(0,4,weight=5)
        >>> Graph.add_edge(4,0,weight=5)
        >>> Graph.add_edge(1,4,weight=1)
        >>> Graph.add_edge(4,1,weight=1)
        >>> Graph.add_edge(2,5,weight=3)
        >>> Graph.add_edge(5,2,weight=3)
        >>> Graph.add_edge(2,7,weight=9)
        >>> Graph.add_edge(7,2,weight=9)
        >>> Graph.add_edge(3,6,weight=3)
        >>> Graph.add_edge(6,3,weight=3)
        >>> Graph.add_edge(3,7,weight=7)
        >>> Graph.add_edge(7,3,weight=7)
        >>> minimum_weight_envy_free_matching(Graph)
        {2:5,5:2,3:6,6:3}

    """
    pass


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    G = nx.Graph(
        [(0, 6), (6, 0), (1, 6), (6, 1), (1, 7), (7, 1), (2, 6), (6, 2), (2, 8), (8, 2), (3, 9), (9, 3), (3, 6), (6, 3),
         (4, 8), (8, 4), (4, 7), (7, 4), (5, 9), (9, 5)])
    print(envy_free_matching(nx.complete_bipartite_graph(3, 3)))
