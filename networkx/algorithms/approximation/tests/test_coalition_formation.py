import math

import pytest

import networkx as nx
from networkx.algorithms.approximation.coalition_formation import match_and_merge


def case_1():
    G = nx.Graph()
    list_of_edges = [(1, 2), (2, 3), (3, 4), (4, 5), (4, 6)]
    G.add_edges_from(list_of_edges)
    return G


def case_5():
    G = nx.Graph()
    list_of_edges = [(1, 2), (2, 3), (3, 1)]
    G.add_edges_from(list_of_edges)
    return G


class Test_coalition_formation:
    def test_1(self):
        G_empty = nx.Graph()
        assert match_and_merge(G_empty, k=0) == []

    def test_2(self):
        G_1 = case_1()
        assert match_and_merge(G_1, k=4) == [[1, 2], [3, 4, 5, 6]]

    def test_3(self):
        G_1 = case_1()
        assert match_and_merge(G_1, k=3) == [[1, 2], [3, 4, 5], [6]]

    def test_4(self):
        G_1 = case_1()
        assert match_and_merge(G_1, k=2) == [[1, 2], [3, 4]]

    def test_5(self):
        G_clique_3 = case_5()
        assert match_and_merge(G_clique_3, k=3) == [[1, 2, 3]]

    def test_6(self):
        # For each n between 5 and 15 (inclusive), generate a clique graph with n nodes and check for 5<k≤15
        for n in range(5, 16):
            G = nx.complete_graph(n)
            for k in range(5, 15):
                if k <= n:
                    P = match_and_merge(G, k)
                    # Check that every partition has at most k nodes
                    assert [len(p) <= k for p in P]

    def test_7(self):
        # Check that every node is in exactly one partition
        for n in range(5, 15):
            G = nx.complete_graph(n)
            for k in range(5, 15):
                if k <= n:
                    P = match_and_merge(G, k)
                    assert [len([p for p in P if n in p]) == 1 for n in G.nodes()]

    def test_8(self):
        # Check that the number of partitions is at most ceil(n/2)
        for n in range(5, 15):
            G = nx.complete_graph(n)
            for k in range(5, 15):
                if k <= n:
                    P = match_and_merge(G, k)
                    assert len(P) <= math.ceil(G.number_of_nodes() / 2)

    def test_9(self):
        # Check that it raises an error when k>n
        for n in range(5, 15):
            G = nx.complete_graph(n)
            for k in range(5, 15):
                if k > n:
                    with pytest.raises(nx.NetworkXError):
                        match_and_merge(G, k)

    def test_10(self):
        # For each n between 5 and 15 (inclusive), generate a random graph with n nodes and check for 5<k≤15
        for n in range(5, 15):
            p = 0.5
            G = nx.gnp_random_graph(n, p)
            for k in range(5, 15):
                if k <= n:
                    P = match_and_merge(G, k)
                    assert [len(p) <= k for p in P]

    def test_11(self):
        # Check that every node is in exactly one partition
        for n in range(5, 15):
            p = 0.5
            G = nx.gnp_random_graph(n, p)
            for k in range(5, 15):
                if k <= n:
                    P = match_and_merge(G, k)
                    assert [len([p for p in P if n in p]) == 1 for n in G.nodes()]
