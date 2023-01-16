"""
Testing the :mod:`networkx.algorithms.approximation.coalition_formation` module.

Which is the implementation of the Social Aware Assignment of Passengers in Ridesharing
The social aware assignment problem belongs to the field of coalition formation, which is an important research branch 
within multiagent systems. It analyses the outcome that results when a set of agents is partitioned into coalitions.
Actually, Match_And_Merge model is a special case of simple Additively Separable Hedonic Games (ASHGs).

Which was described in the article:
Levinger C., Hazon N., Azaria A. Social Aware Assignment of Passengers in Ridesharing. - 2022, http://azariaa.com/Content/Publications/Social_Assignment_SA.pdf.

The match_and_merge algorithm is based on the pseudocode from the article
which is written (as well as the tests) by Victor Kushnir.
"""
import math

import pytest

import networkx as nx
from networkx.algorithms.approximation.coalition_formation import match_and_merge


def small_chain_graph():
    G = nx.Graph()
    list_of_edges = [(1, 2), (2, 3), (3, 4), (4, 5), (4, 6)]
    G.add_edges_from(list_of_edges)
    return G


def clique_graph_of_size_3():
    G = nx.Graph()
    list_of_edges = [(1, 2), (2, 3), (3, 1)]
    G.add_edges_from(list_of_edges)
    return G


class Test_coalition_formation:
    def test_empty_graph_returns_empty_list(self):
        G_empty = nx.Graph()
        assert match_and_merge(G_empty, k=0) == []

    def test_small_chain_graph_with_k_4_returns_correct_partition(self):
        G_1 = small_chain_graph()
        assert match_and_merge(G_1, k=4) == [[1, 2], [3, 4, 5, 6]]

    def test_small_chain_graph_with_k_3_returns_correct_partition(self):
        G_1 = small_chain_graph()
        assert match_and_merge(G_1, k=3) == [[1, 2], [3, 4, 5], [6]]

    def test_small_chain_graph_with_k_2_returns_correct_partition(self):
        G_1 = small_chain_graph()
        assert match_and_merge(G_1, k=2) == [[1, 2], [3, 4]]

    def test_clique_graph_of_size_3_with_k_3_returns_correct_partition(self):
        G_clique_3 = clique_graph_of_size_3()
        assert match_and_merge(G_clique_3, k=3) == [[1, 2, 3]]

    def test_clique_graph_with_k_in_range_returns_correct_partition(self):
        # For each n between 5 and 15 (inclusive), generate a clique graph with n nodes and check for 5<k≤15
        for n in range(5, 16):
            G = nx.complete_graph(n)
            for k in range(5, 15):
                if k <= n:
                    P = match_and_merge(G, k)
                    # Check that every partition has at most k nodes
                    assert [len(p) <= k for p in P]

    def test_clique_graph_with_k_in_range_every_node_in_exactly_one_partition(self):
        # Check that every node is in exactly one partition
        for n in range(5, 15):
            G = nx.complete_graph(n)
            for k in range(5, 15):
                if k <= n:
                    P = match_and_merge(G, k)
                    assert [len([p for p in P if n in p]) == 1 for n in G.nodes()]

    def test_clique_graph_with_k_in_range_number_of_partitions_at_most_ceil_n_2(self):
        # Check that the number of partitions is at most ceil(n/2)
        for n in range(5, 15):
            G = nx.complete_graph(n)
            for k in range(5, 15):
                if k <= n:
                    P = match_and_merge(G, k)
                    assert len(P) <= math.ceil(G.number_of_nodes() / 2)

    def test_k_greater_than_n_raises_error(self):
        # Check that it raises an error when k>n
        for n in range(5, 15):
            G = nx.complete_graph(n)
            for k in range(5, 15):
                if k > n:
                    with pytest.raises(nx.NetworkXError):
                        match_and_merge(G, k)

    def test_random_graph_with_k_in_range_returns_correct_partition(self):
        # For each n between 5 and 15 (inclusive), generate a random graph with n nodes and check for 5<k≤15
        for n in range(5, 15):
            p = 0.5
            G = nx.gnp_random_graph(n, p)
            for k in range(5, 15):
                if k <= n:
                    P = match_and_merge(G, k)
                    assert [len(p) <= k for p in P]

    def test_random_graph_with_k_in_range_every_node_in_exactly_one_partition(self):
        # Check that every node is in exactly one partition
        for n in range(5, 15):
            p = 0.5
            G = nx.gnp_random_graph(n, p)
            for k in range(5, 15):
                if k <= n:
                    P = match_and_merge(G, k)
                    assert [len([p for p in P if n in p]) == 1 for n in G.nodes()]
