import pytest
import networkx as nx
import itertools
import math
from networkx.algorithms.approximation.social_aware_assignment_of_passengers_in_ridesharing import match_and_merge, find_matching


def case_1():
    G = nx.Graph()
    list_of_edges = [(1, 2), (2, 3), (3, 4), (4, 5), (4, 6)]
    G.add_edges_from(list_of_edges)
    k = 4
    return G, k


def case_2():
    G = nx.Graph()
    list_of_edges = [(1, 2), (2, 3), (3, 1)]
    G.add_edges_from(list_of_edges)
    k = 3
    return G, k


def case_3():
    G = nx.Graph()
    list_of_edges = [(1, 2), (1, 3), (1, 5), (1, 6), (2, 4), (2, 7), (3, 4), (3, 5), (3, 6), (4, 5), (4, 6), (4, 7), (5, 8), (6, 7), (6, 8)]
    G.add_edges_from(list_of_edges)
    k = 3
    return G, k


class test_social_aware_assignment_of_passengers_in_ridesharing:

    def test_mnm_empty_graph(self):
        G = nx.Graph()
        k = 5
        assert match_and_merge(G, k) == []

    def test_fm_empty_graph(self):
        G = nx.Graph()
        l = 5
        Opt = []
        assert find_matching(G, l, Opt) == []

    def test_1(self):
        G, k = case_1()
        P = match_and_merge(G, k)
        assert P == [[1, 2], [3, 4, 5, 6]]
        assert find_matching(G, k-1, P) == []

    def test_2(self):
        G, k = case_2()
        P = match_and_merge(G, k)
        assert match_and_merge(G, k) == [[1, 2, 3]]
        assert find_matching(G, k-1, P) == [[1, 2], [2, 3], [3, 1]]

    def test_3(self):
        G, k = case_3()
        P = match_and_merge(G, k)
        assert P == [[1, 2, 3], [4, 5, 6], [7, 8]]
        assert find_matching(G, k, P) in [[1, 2, 3], [4, 5, 6]]

    def test_4(self):
        # For each n between 5 and 15 (inclusive), generate a clique graph with n nodes and check for 5<k≤15
        for n in range(5, 15):
            G = nx.complete_graph(n)
            for k in range(5, 15):
                if k<=n:
                    P = match_and_merge(G, k)
                    assert len(P) == math.ceil(math.log(n, k))
                    assert find_matching(G, k-1, P) in itertools.combinations(G.nodes(), k-1)
                else:
                    with pytest.raises(nx.NetworkXError):
                        match_and_merge(G, k)




