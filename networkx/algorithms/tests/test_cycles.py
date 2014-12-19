#!/usr/bin/env python
from nose.tools import *
import networkx
import networkx as nx

from networkx.algorithms import find_cycle
FORWARD = nx.algorithms.edgedfs.FORWARD
REVERSE = nx.algorithms.edgedfs.REVERSE


class TestCycles:

    def setUp(self):
        G = networkx.Graph()
        G.add_cycle([0, 1, 2, 3])
        G.add_cycle([0, 3, 4, 5])
        G.add_cycle([0, 1, 6, 7, 8])
        G.add_edge(8, 9)
        self.G = G

    def is_cyclic_permutation(self, a, b):
        n = len(a)
        if len(b) != n:
            return False
        l = a + a
        return any(l[i:i + n] == b for i in range(2 * n - n + 1))

    def test_cycle_basis(self):
        G = self.G
        cy = networkx.cycle_basis(G, 0)
        sort_cy = sorted(sorted(c) for c in cy)
        assert_equal(sort_cy, [[0, 1, 2, 3], [0, 1, 6, 7, 8], [0, 3, 4, 5]])
        cy = networkx.cycle_basis(G, 1)
        sort_cy = sorted(sorted(c) for c in cy)
        assert_equal(sort_cy, [[0, 1, 2, 3], [0, 1, 6, 7, 8], [0, 3, 4, 5]])
        cy = networkx.cycle_basis(G, 9)
        sort_cy = sorted(sorted(c) for c in cy)
        assert_equal(sort_cy, [[0, 1, 2, 3], [0, 1, 6, 7, 8], [0, 3, 4, 5]])
        # test disconnected graphs
        G.add_cycle(list("ABC"))
        cy = networkx.cycle_basis(G, 9)
        sort_cy = sorted(sorted(c) for c in cy[:-1]) + [sorted(cy[-1])]
        assert_equal(
            sort_cy, [
                [
                    0, 1, 2, 3], [
                    0, 1, 6, 7, 8], [
                    0, 3, 4, 5], [
                        'A', 'B', 'C']])

    @raises(nx.NetworkXNotImplemented)
    def test_cycle_basis(self):
        G = nx.DiGraph()
        cy = networkx.cycle_basis(G, 0)

    @raises(nx.NetworkXNotImplemented)
    def test_cycle_basis(self):
        G = nx.MultiGraph()
        cy = networkx.cycle_basis(G, 0)

    def test_simple_cycles(self):
        G = nx.DiGraph(
            [(0, 0), (0, 1), (0, 2), (1, 2), (2, 0), (2, 1), (2, 2)])
        cc = sorted(nx.simple_cycles(G))
        ca = [[0], [0, 1, 2], [0, 2], [1, 2], [2]]
        for c in cc:
            assert_true(any(self.is_cyclic_permutation(c, rc) for rc in ca))

    @raises(nx.NetworkXNotImplemented)
    def test_simple_cycles_graph(self):
        G = nx.Graph()
        c = sorted(nx.simple_cycles(G))

    def test_unsortable(self):
        #  TODO What does this test do?  das 6/2013
        G = nx.DiGraph()
        G.add_cycle(['a', 1])
        c = list(nx.simple_cycles(G))

    def test_simple_cycles_small(self):
        G = nx.DiGraph()
        G.add_cycle([1, 2, 3])
        c = sorted(nx.simple_cycles(G))
        assert_equal(len(c), 1)
        assert_true(self.is_cyclic_permutation(c[0], [1, 2, 3]))
        G.add_cycle([10, 20, 30])
        cc = sorted(nx.simple_cycles(G))
        ca = [[1, 2, 3], [10, 20, 30]]
        for c in cc:
            assert_true(any(self.is_cyclic_permutation(c, rc) for rc in ca))

    def test_simple_cycles_empty(self):
        G = nx.DiGraph()
        assert_equal(list(nx.simple_cycles(G)), [])

    def test_complete_directed_graph(self):
        # see table 2 in Johnson's paper
        ncircuits = [1, 5, 20, 84, 409, 2365, 16064]
        for n, c in zip(range(2, 9), ncircuits):
            G = nx.DiGraph(nx.complete_graph(n))
            assert_equal(len(list(nx.simple_cycles(G))), c)

    def worst_case_graph(self, k):
        # see figure 1 in Johnson's paper
        # this graph has excactly 3k simple cycles
        G = nx.DiGraph()
        for n in range(2, k + 2):
            G.add_edge(1, n)
            G.add_edge(n, k + 2)
        G.add_edge(2 * k + 1, 1)
        for n in range(k + 2, 2 * k + 2):
            G.add_edge(n, 2 * k + 2)
            G.add_edge(n, n + 1)
        G.add_edge(2 * k + 3, k + 2)
        for n in range(2 * k + 3, 3 * k + 3):
            G.add_edge(2 * k + 2, n)
            G.add_edge(n, 3 * k + 3)
        G.add_edge(3 * k + 3, 2 * k + 2)
        return G

    def test_worst_case_graph(self):
        # see figure 1 in Johnson's paper
        for k in range(3, 10):
            G = self.worst_case_graph(k)
            l = len(list(nx.simple_cycles(G)))
            assert_equal(l, 3 * k)

    def test_recursive_simple_and_not(self):
        for k in range(2, 10):
            G = self.worst_case_graph(k)
            cc = sorted(nx.simple_cycles(G))
            rcc = sorted(nx.recursive_simple_cycles(G))
            assert_equal(len(cc), len(rcc))
            for c in cc:
                assert_true(any(self.is_cyclic_permutation(c, rc)
                                for rc in rcc))
            for rc in rcc:
                assert_true(any(self.is_cyclic_permutation(rc, c) for c in cc))

    def test_simple_graph_with_reported_bug(self):
        G = nx.DiGraph()
        edges = [(0, 2), (0, 3), (1, 0), (1, 3), (2, 1), (2, 4),
                 (3, 2), (3, 4), (4, 0), (4, 1), (4, 5), (5, 0),
                 (5, 1), (5, 2), (5, 3)]
        G.add_edges_from(edges)
        cc = sorted(nx.simple_cycles(G))
        assert_equal(len(cc), 26)
        rcc = sorted(nx.recursive_simple_cycles(G))
        assert_equal(len(cc), len(rcc))
        for c in cc:
            assert_true(any(self.is_cyclic_permutation(c, rc) for rc in rcc))
        for rc in rcc:
            assert_true(any(self.is_cyclic_permutation(rc, c) for c in cc))

# These tests might fail with hash randomization since they depend on
# edge_dfs. For more information, see the comments in:
#    networkx/algorithms/traversal/tests/test_edgedfs.py


class TestFindCycle(object):

    def setUp(self):
        self.nodes = [0, 1, 2, 3]
        self.edges = [(-1, 0), (0, 1), (1, 0), (1, 0), (2, 1), (3, 1)]

    def test_graph(self):
        G = nx.Graph(self.edges)
        assert_raises(nx.exception.NetworkXNoCycle, find_cycle, G, self.nodes)

    def test_digraph(self):
        G = nx.DiGraph(self.edges)
        x = list(find_cycle(G, self.nodes))
        x_ = [(0, 1), (1, 0)]
        assert_equal(x, x_)

    def test_multigraph(self):
        G = nx.MultiGraph(self.edges)
        x = list(find_cycle(G, self.nodes))
        x_ = [(0, 1, 0), (1, 0, 1)]  # or (1, 0, 2)
        # Hash randomization...could be any edge.
        assert_equal(x[0], x_[0])
        assert_equal(x[1][:2], x_[1][:2])

    def test_multidigraph(self):
        G = nx.MultiDiGraph(self.edges)
        x = list(find_cycle(G, self.nodes))
        x_ = [(0, 1, 0), (1, 0, 0)]  # (1, 0, 1)
        assert_equal(x[0], x_[0])
        assert_equal(x[1][:2], x_[1][:2])

    def test_digraph_ignore(self):
        G = nx.DiGraph(self.edges)
        x = list(find_cycle(G, self.nodes, orientation='ignore'))
        x_ = [(0, 1, FORWARD), (1, 0, FORWARD)]
        assert_equal(x, x_)

    def test_multidigraph_ignore(self):
        G = nx.MultiDiGraph(self.edges)
        x = list(find_cycle(G, self.nodes, orientation='ignore'))
        x_ = [(0, 1, 0, FORWARD), (1, 0, 0, FORWARD)]  # or (1, 0, 1, 1)
        assert_equal(x[0], x_[0])
        assert_equal(x[1][:2], x_[1][:2])
        assert_equal(x[1][3], x_[1][3])

    def test_multidigraph_ignore2(self):
        # Loop traversed an edge while ignoring its orientation.
        G = nx.MultiDiGraph([(0, 1), (1, 2), (1, 2)])
        x = list(find_cycle(G, [0, 1, 2], orientation='ignore'))
        x_ = [(1, 2, 0, FORWARD), (1, 2, 1, REVERSE)]
        assert_equal(x, x_)

    def test_multidigraph_ignore2(self):
        # Node 2 doesn't need to be searched again from visited from 4.
        # The goal here is to cover the case when 2 to be researched from 4,
        # when 4 is visited from the first time (so we must make sure that 4
        # is not visited from 2, and hence, we respect the edge orientation).
        G = nx.MultiDiGraph([(0, 1), (1, 2), (2, 3), (4, 2)])
        assert_raises(nx.exception.NetworkXNoCycle,
                      find_cycle, G, [0, 1, 2, 3, 4], orientation='original')

    def test_dag(self):
        G = nx.DiGraph([(0, 1), (0, 2), (1, 2)])
        assert_raises(nx.exception.NetworkXNoCycle,
                      find_cycle, G, orientation='original')
        x = list(find_cycle(G, orientation='ignore'))
        assert_equal(x, [(0, 1, FORWARD), (1, 2, FORWARD), (0, 2, REVERSE)])
