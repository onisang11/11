import math
import pytest
import networkx as nx
from networkx.algorithms.approximation.social_aware_assignment_of_passengers_in_ridesharing import (
    match_and_merge,
)


def case_1():
    G = nx.Graph()
    list_of_edges = [(1, 2), (2, 3), (3, 4), (4, 5), (4, 6)]
    G.add_edges_from(list_of_edges)
    k = 4
    return G, k


def case_5():
    G = nx.Graph()
    list_of_edges = [(1, 2), (2, 3), (3, 1)]
    G.add_edges_from(list_of_edges)
    k = 3
    return G, k


class Test_social_aware_assignment_of_passengers_in_ridesharing:
    def test_1(self):
        G = nx.Graph()
        k = 0
        assert match_and_merge(G, k) == []

    def test_2(self):
        G, k = case_1()
        assert match_and_merge(G, k) == [[1, 2], [3, 4, 5, 6]]

    def test_3(self):
        G, k = case_1()
        k = 3
        print(match_and_merge(G, k))
        assert match_and_merge(G, k) == [[1, 2], [3, 4, 5], [6]]

    def test_4(self):
        G, k = case_1()
        k = 2
        assert match_and_merge(G, k) == [[1, 2], [3, 4]]

    def test_5(self):
        G, k = case_5()
        assert match_and_merge(G, k) == [[1, 2, 3]]

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
