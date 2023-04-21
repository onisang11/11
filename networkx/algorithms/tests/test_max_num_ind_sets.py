"""
Tests for maximum number of independent sets.
"""

import networkx as nx
import networkx.algorithms.max_num_ind_sets as ug
import pytest

def test_singleton_graph():
    G = ug.UCIGraph()
    G.add_node(1)
    assert G.num_independent_sets() == 2

def test_len2_path():
    G = ug.UCIGraph()
    G.add_node(1)
    G.add_node(2)
    G.add_edge(1, 2)
    assert G.num_independent_sets() == 3


def test_simple_path_tree():
    G = ug.UCIGraph()
    G.add_node(1)#2
    G.add_node(2)#3
    G.add_node(3)#5
    G.add_node(4)#8
    G.add_node(5)#13
    G.add_edge(1, 2)
    G.add_edge(2, 3)
    G.add_edge(3, 4)
    G.add_edge(4, 5)
    assert G.num_independent_sets() == 13

def test_simple_path_tree2():
    G = ug.UCIGraph()
    G.add_node(1)#2
    G.add_node(2)#3
    G.add_node(3)#5
    G.add_node(4)#8
    G.add_node(5)#13
    G.add_node(6)#21
    G.add_edge(1, 2)
    G.add_edge(2, 3)
    G.add_edge(3, 4)
    G.add_edge(4, 5)
    G.add_edge(5, 6)
    assert G.num_independent_sets() == 21

def test_binary_tree_of_depth_3():
    G = ug.UCIGraph()
    G.add_node(1)
    G.add_node(2)
    G.add_node(3)
    G.add_edge(1, 2)
    G.add_edge(1, 3)

    G.add_node(4)
    G.add_node(5)
    G.add_node(6)
    G.add_node(7)
    G.add_edge(2, 4)
    G.add_edge(2, 5)
    G.add_edge(3, 6)
    G.add_edge(3, 7)
    assert G.num_independent_sets() == 41

def test_tree_of_depth_3():
    G = ug.UCIGraph()
    G.add_node(1)
    G.add_node(2)
    G.add_node(3)
    G.add_node(4)
    G.add_edge(1, 2)
    G.add_edge(1, 3)
    G.add_edge(1, 4)

    G.add_node(5)
    G.add_node(6)
    G.add_node(7)
    G.add_node(8)
    G.add_edge(2, 5)
    G.add_edge(2, 6)
    G.add_edge(3, 7)
    G.add_edge(4, 8)
    assert G.num_independent_sets() == 61

def test_tree_of_depth_4(): #add a node on top
    G = ug.UCIGraph()
    G.add_node(0)
    G.add_node(1)
    G.add_edge(0, 1)

    G.add_node(2)
    G.add_node(3)
    G.add_node(4)
    G.add_edge(1, 2)
    G.add_edge(1, 3)
    G.add_edge(1, 4)

    G.add_node(5)
    G.add_node(6)
    G.add_node(7)
    G.add_node(8)
    G.add_edge(2, 5)
    G.add_edge(2, 6)
    G.add_edge(3, 7)
    G.add_edge(4, 8)
    assert G.num_independent_sets() == 106

