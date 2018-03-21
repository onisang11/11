from nose.tools import assert_equals
import networkx as nx


class SmokeTestOrdered(object):
    # Just test instantiation.
    def test_graph(self):
        G = nx.OrderedGraph()

    def test_digraph(self):
        G = nx.OrderedDiGraph()

    def test_multigraph(self):
        G = nx.OrderedMultiGraph()

    def test_multidigraph(self):
        G = nx.OrderedMultiDiGraph()


class TestOrderedFeatures(object):
    def setUp(self):
        self.G = nx.OrderedDiGraph()
        # The nodes should not be in numerical order, some operations may
        # sort the keys and expecting them sorted masks this unwanted
        # behavior.
        self.G.add_nodes_from([2, 3, 1])
        self.G.add_edges_from([(2, 3), (1, 3)])

    def test_subgraph_order(self):
        G = self.G
        G_sub = G.subgraph([2, 3, 1, 3])
        assert_equals(list(G.nodes), list(G_sub.nodes))
        assert_equals(list(G.edges), list(G_sub.edges))
        assert_equals(list(G.pred[3]), list(G_sub.pred[3]))
        assert_equals([2, 1], list(G_sub.pred[3]))
        assert_equals([], list(G_sub.succ[3]))

        G_sub = nx.induced_subgraph(G, [2, 3, 1, 3])
        assert_equals(list(G.nodes), list(G_sub.nodes))
        assert_equals(list(G.edges), list(G_sub.edges))
        assert_equals(list(G.pred[3]), list(G_sub.pred[3]))
        assert_equals([2, 1], list(G_sub.pred[3]))
        assert_equals([], list(G_sub.succ[3]))
