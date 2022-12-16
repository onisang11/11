import pytest
import networkx as nx
import math
from networkx.algorithms.approximation.social_aware_assignment_of_passengers_in_ridesharing import match_and_merge


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






class Test_social_aware_assignment_of_passengers_in_ridesharing:

    def test_mnm_empty_graph(self):
        G = nx.Graph()
        k = 5
        assert match_and_merge(G, k) == []

    def test_mnm_1(self):
        G, k = case_1()
        assert match_and_merge(G, k) == [[1, 2], [3, 4, 5, 6]]

    def test_mnm_2(self):
        G, k = case_2()
        assert match_and_merge(G, k) == [[1, 2, 3]]

    def test_mnm_3(self):
        G, k = case_3()
        assert match_and_merge(G, k) == [[1, 2, 3], [4, 5, 6], [7, 8]]

    def test_4(self):
        # For each n between 5 and 15 (inclusive), generate a clique graph with n nodes and check for 5<k≤15
        for n in range(5, 15):
            G = nx.complete_graph(n)
            for k in range(5, 15):
                if k <= n:
                    P = match_and_merge(G, k)
                    assert len(P) == math.ceil(n/k)
                else:
                    with pytest.raises(nx.NetworkXError):
                        match_and_merge(G, k)




