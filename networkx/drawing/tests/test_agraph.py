"""Unit tests for PyGraphviz interface."""
import os
import tempfile
import pytest

pygraphviz = pytest.importorskip("pygraphviz")


from networkx.testing import assert_edges_equal, assert_nodes_equal, assert_graphs_equal

import networkx as nx


class TestAGraph:
    def build_graph(self, G):
        edges = [("A", "B"), ("A", "C"), ("A", "C"), ("B", "C"), ("A", "D")]
        G.add_edges_from(edges)
        G.add_node("E")
        G.graph["metal"] = "bronze"
        return G

    def assert_equal(self, G1, G2):
        assert_nodes_equal(G1.nodes(), G2.nodes())
        assert_edges_equal(G1.edges(), G2.edges())
        assert G1.graph["metal"] == G2.graph["metal"]

    def agraph_checks(self, G):
        G = self.build_graph(G)
        A = nx.nx_agraph.to_agraph(G)
        H = nx.nx_agraph.from_agraph(A)
        self.assert_equal(G, H)

        fname = tempfile.mktemp()
        nx.drawing.nx_agraph.write_dot(H, fname)
        Hin = nx.nx_agraph.read_dot(fname)
        os.unlink(fname)
        self.assert_equal(H, Hin)

        (fd, fname) = tempfile.mkstemp()
        with open(fname, "w") as fh:
            nx.drawing.nx_agraph.write_dot(H, fh)

        with open(fname) as fh:
            Hin = nx.nx_agraph.read_dot(fh)
        os.unlink(fname)
        self.assert_equal(H, Hin)

    def test_from_agraph_name(self):
        G = nx.Graph(name="test")
        A = nx.nx_agraph.to_agraph(G)
        H = nx.nx_agraph.from_agraph(A)
        assert G.name == "test"

    @pytest.mark.parametrize(
        "graph_class", (nx.Graph, nx.DiGraph, nx.MultiGraph, nx.MultiDiGraph,)
    )
    def test_from_agraph_create_using(self, graph_class):
        G = nx.path_graph(3)
        A = nx.nx_agraph.to_agraph(G)
        H = nx.nx_agraph.from_agraph(A, create_using=graph_class)
        assert type(H) == graph_class

    def test_undirected(self):
        self.agraph_checks(nx.Graph())

    def test_directed(self):
        self.agraph_checks(nx.DiGraph())

    def test_multi_undirected(self):
        self.agraph_checks(nx.MultiGraph())

    def test_multi_directed(self):
        self.agraph_checks(nx.MultiDiGraph())

    def test_to_agraph_with_nodedata(self):
        G = nx.Graph()
        G.add_node(1, color="red")
        A = nx.nx_agraph.to_agraph(G)
        assert dict(A.nodes()[0].attr) == {"color": "red"}

    @pytest.mark.parametrize("graph_class", (nx.Graph, nx.MultiGraph))
    def test_to_agraph_with_edgedata(self, graph_class):
        G = graph_class()
        G.add_nodes_from([0, 1])
        G.add_edge(0, 1, color="yellow")
        A = nx.nx_agraph.to_agraph(G)
        assert dict(A.edges()[0].attr) == {"color": "yellow"}

    def test_view_pygraphviz(self):
        G = nx.Graph()  # "An empty graph cannot be drawn."
        pytest.raises(nx.NetworkXException, nx.nx_agraph.view_pygraphviz, G)
        G = nx.barbell_graph(4, 6)
        nx.nx_agraph.view_pygraphviz(G)

    def test_view_pygraphviz_edgelabel(self):
        G = nx.Graph()
        G.add_edge(1, 2, weight=7)
        G.add_edge(2, 3, weight=8)
        nx.nx_agraph.view_pygraphviz(G, edgelabel="weight")

    def test_graph_with_reserved_keywords(self):
        # test attribute/keyword clash case for #1582
        # node: n
        # edges: u,v
        G = nx.Graph()
        G = self.build_graph(G)
        G.nodes["E"]["n"] = "keyword"
        G.edges[("A", "B")]["u"] = "keyword"
        G.edges[("A", "B")]["v"] = "keyword"
        A = nx.nx_agraph.to_agraph(G)

    def test_round_trip_empty_graph(self):
        G = nx.Graph()
        A = nx.nx_agraph.to_agraph(G)
        H = nx.nx_agraph.from_agraph(A)
        # assert_graphs_equal(G, H)
        AA = nx.nx_agraph.to_agraph(H)
        HH = nx.nx_agraph.from_agraph(AA)
        assert_graphs_equal(H, HH)
        G.graph["graph"] = {}
        G.graph["node"] = {}
        G.graph["edge"] = {}
        assert_graphs_equal(G, HH)

    @pytest.mark.xfail(reason="integer->string node conversion in round trip")
    def test_round_trip_integer_nodes(self):
        G = nx.complete_graph(3)
        A = nx.nx_agraph.to_agraph(G)
        H = nx.nx_agraph.from_agraph(A)
        assert_graphs_equal(G, H)

    def test_2d_layout(self):
        G = nx.Graph()
        G = self.build_graph(G)
        G.graph["dimen"] = 2
        pos = nx.nx_agraph.pygraphviz_layout(G, prog="neato")
        pos = list(pos.values())
        assert len(pos) == 5
        assert len(pos[0]) == 2

    def test_3d_layout(self):
        G = nx.Graph()
        G = self.build_graph(G)
        G.graph["dimen"] = 3
        pos = nx.nx_agraph.pygraphviz_layout(G, prog="neato")
        pos = list(pos.values())
        assert len(pos) == 5
        assert len(pos[0]) == 3
