import pytest
import networkx as nx
from networkx.testing import assert_edges_equal


def test_union_attributes():
    g = nx.Graph()
    g.add_node(0, x=4)
    g.add_node(1, x=5)
    g.add_edge(0, 1, size=5)
    g.graph["name"] = "g"

    h = g.copy()
    h.graph["name"] = "h"
    h.graph["attr"] = "attr"
    h.nodes[0]["x"] = 7

    gh = nx.union(g, h, rename=("g", "h"))
    assert set(gh.nodes()) == {"h0", "h1", "g0", "g1"}
    for n in gh:
        graph, node = n
        assert gh.nodes[n] == eval(graph).nodes[int(node)]

    assert gh.graph["attr"] == "attr"
    assert gh.graph["name"] == "h"  # h graph attributes take precendent


def test_intersection():
    G = nx.Graph()
    H = nx.Graph()
    G.add_nodes_from([1, 2, 3, 4])
    G.add_edge(1, 2)
    G.add_edge(2, 3)
    H.add_nodes_from([1, 2, 3, 4])
    H.add_edge(2, 3)
    H.add_edge(3, 4)
    I = nx.intersection(G, H)
    assert set(I.nodes()) == {1, 2, 3, 4}
    assert sorted(I.edges()) == [(2, 3)]


def test_intersection_attributes():
    g = nx.Graph()
    g.add_node(0, x=4)
    g.add_node(1, x=5)
    g.add_edge(0, 1, size=5)
    g.graph["name"] = "g"

    h = g.copy()
    h.graph["name"] = "h"
    h.graph["attr"] = "attr"
    h.nodes[0]["x"] = 7

    gh = nx.intersection(g, h)
    assert set(gh.nodes()) == set(g.nodes())
    assert set(gh.nodes()) == set(h.nodes())
    assert sorted(gh.edges()) == sorted(g.edges())

    h.remove_node(0)
    pytest.raises(nx.NetworkXError, nx.intersection, g, h)


def test_intersection_multigraph_attributes():
    g = nx.MultiGraph()
    g.add_edge(0, 1, key=0)
    g.add_edge(0, 1, key=1)
    g.add_edge(0, 1, key=2)
    h = nx.MultiGraph()
    h.add_edge(0, 1, key=0)
    h.add_edge(0, 1, key=3)
    gh = nx.intersection(g, h)
    assert set(gh.nodes()) == set(g.nodes())
    assert set(gh.nodes()) == set(h.nodes())
    assert sorted(gh.edges()) == [(0, 1)]
    assert sorted(gh.edges(keys=True)) == [(0, 1, 0)]


def test_difference():
    G = nx.Graph()
    H = nx.Graph()
    G.add_nodes_from([1, 2, 3, 4])
    G.add_edge(1, 2)
    G.add_edge(2, 3)
    H.add_nodes_from([1, 2, 3, 4])
    H.add_edge(2, 3)
    H.add_edge(3, 4)
    D = nx.difference(G, H)
    assert set(D.nodes()) == {1, 2, 3, 4}
    assert sorted(D.edges()) == [(1, 2)]
    D = nx.difference(H, G)
    assert set(D.nodes()) == {1, 2, 3, 4}
    assert sorted(D.edges()) == [(3, 4)]
    D = nx.symmetric_difference(G, H)
    assert set(D.nodes()) == {1, 2, 3, 4}
    assert sorted(D.edges()) == [(1, 2), (3, 4)]


def test_difference2():
    G = nx.Graph()
    H = nx.Graph()
    G.add_nodes_from([1, 2, 3, 4])
    H.add_nodes_from([1, 2, 3, 4])
    G.add_edge(1, 2)
    H.add_edge(1, 2)
    G.add_edge(2, 3)
    D = nx.difference(G, H)
    assert set(D.nodes()) == {1, 2, 3, 4}
    assert sorted(D.edges()) == [(2, 3)]
    D = nx.difference(H, G)
    assert set(D.nodes()) == {1, 2, 3, 4}
    assert sorted(D.edges()) == []
    H.add_edge(3, 4)
    D = nx.difference(H, G)
    assert set(D.nodes()) == {1, 2, 3, 4}
    assert sorted(D.edges()) == [(3, 4)]


def test_difference_attributes():
    g = nx.Graph()
    g.add_node(0, x=4)
    g.add_node(1, x=5)
    g.add_edge(0, 1, size=5)
    g.graph["name"] = "g"

    h = g.copy()
    h.graph["name"] = "h"
    h.graph["attr"] = "attr"
    h.nodes[0]["x"] = 7

    gh = nx.difference(g, h)
    assert set(gh.nodes()) == set(g.nodes())
    assert set(gh.nodes()) == set(h.nodes())
    assert sorted(gh.edges()) == []

    h.remove_node(0)
    pytest.raises(nx.NetworkXError, nx.intersection, g, h)


def test_difference_multigraph_attributes():
    g = nx.MultiGraph()
    g.add_edge(0, 1, key=0)
    g.add_edge(0, 1, key=1)
    g.add_edge(0, 1, key=2)
    h = nx.MultiGraph()
    h.add_edge(0, 1, key=0)
    h.add_edge(0, 1, key=3)
    gh = nx.difference(g, h)
    assert set(gh.nodes()) == set(g.nodes())
    assert set(gh.nodes()) == set(h.nodes())
    assert sorted(gh.edges()) == [(0, 1), (0, 1)]
    assert sorted(gh.edges(keys=True)) == [(0, 1, 1), (0, 1, 2)]


def test_difference_raise():
    G = nx.path_graph(4)
    H = nx.path_graph(3)
    pytest.raises(nx.NetworkXError, nx.difference, G, H)
    pytest.raises(nx.NetworkXError, nx.symmetric_difference, G, H)


def test_symmetric_difference_multigraph():
    g = nx.MultiGraph()
    g.add_edge(0, 1, key=0)
    g.add_edge(0, 1, key=1)
    g.add_edge(0, 1, key=2)
    h = nx.MultiGraph()
    h.add_edge(0, 1, key=0)
    h.add_edge(0, 1, key=3)
    gh = nx.symmetric_difference(g, h)
    assert set(gh.nodes()) == set(g.nodes())
    assert set(gh.nodes()) == set(h.nodes())
    assert sorted(gh.edges()) == 3 * [(0, 1)]
    assert sorted(sorted(e) for e in gh.edges(keys=True)) == [
        [0, 1, 1],
        [0, 1, 2],
        [0, 1, 3],
    ]


def test_union_and_compose():
    K3 = nx.complete_graph(3)
    P3 = nx.path_graph(3)

    G1 = nx.DiGraph()
    G1.add_edge("A", "B")
    G1.add_edge("A", "C")
    G1.add_edge("A", "D")
    G2 = nx.DiGraph()
    G2.add_edge("1", "2")
    G2.add_edge("1", "3")
    G2.add_edge("1", "4")

    G = nx.union(G1, G2)
    H = nx.compose(G1, G2)
    assert_edges_equal(G.edges(), H.edges())
    assert not G.has_edge("A", 1)
    pytest.raises(nx.NetworkXError, nx.union, K3, P3)
    H1 = nx.union(H, G1, rename=("H", "G1"))
    assert sorted(H1.nodes()) == [
        "G1A",
        "G1B",
        "G1C",
        "G1D",
        "H1",
        "H2",
        "H3",
        "H4",
        "HA",
        "HB",
        "HC",
        "HD",
    ]

    H2 = nx.union(H, G2, rename=("H", ""))
    assert sorted(H2.nodes()) == [
        "1",
        "2",
        "3",
        "4",
        "H1",
        "H2",
        "H3",
        "H4",
        "HA",
        "HB",
        "HC",
        "HD",
    ]

    assert not H1.has_edge("NB", "NA")

    G = nx.compose(G, G)
    assert_edges_equal(G.edges(), H.edges())

    G2 = nx.union(G2, G2, rename=("", "copy"))
    assert sorted(G2.nodes()) == [
        "1",
        "2",
        "3",
        "4",
        "copy1",
        "copy2",
        "copy3",
        "copy4",
    ]

    assert sorted(G2.neighbors("copy4")) == []
    assert sorted(G2.neighbors("copy1")) == ["copy2", "copy3", "copy4"]
    assert len(G) == 8
    assert nx.number_of_edges(G) == 6

    E = nx.disjoint_union(G, G)
    assert len(E) == 16
    assert nx.number_of_edges(E) == 12

    E = nx.disjoint_union(G1, G2)
    assert sorted(E.nodes()) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

    G = nx.Graph()
    H = nx.Graph()
    G.add_nodes_from([(1, {"a1": 1})])
    H.add_nodes_from([(1, {"b1": 1})])
    R = nx.compose(G, H)
    assert R.nodes == {1: {"a1": 1, "b1": 1}}


def test_union_multigraph():
    G = nx.MultiGraph()
    G.add_edge(1, 2, key=0)
    G.add_edge(1, 2, key=1)
    H = nx.MultiGraph()
    H.add_edge(3, 4, key=0)
    H.add_edge(3, 4, key=1)
    GH = nx.union(G, H)
    assert set(GH) == set(G) | set(H)
    assert set(GH.edges(keys=True)) == set(G.edges(keys=True)) | set(H.edges(keys=True))


def test_disjoint_union_multigraph():
    G = nx.MultiGraph()
    G.add_edge(0, 1, key=0)
    G.add_edge(0, 1, key=1)
    H = nx.MultiGraph()
    H.add_edge(2, 3, key=0)
    H.add_edge(2, 3, key=1)
    GH = nx.disjoint_union(G, H)
    assert set(GH) == set(G) | set(H)
    assert set(GH.edges(keys=True)) == set(G.edges(keys=True)) | set(H.edges(keys=True))


def test_compose_multigraph():
    G = nx.MultiGraph()
    G.add_edge(1, 2, key=0)
    G.add_edge(1, 2, key=1)
    H = nx.MultiGraph()
    H.add_edge(3, 4, key=0)
    H.add_edge(3, 4, key=1)
    GH = nx.compose(G, H)
    assert set(GH) == set(G) | set(H)
    assert set(GH.edges(keys=True)) == set(G.edges(keys=True)) | set(H.edges(keys=True))
    H.add_edge(1, 2, key=2)
    GH = nx.compose(G, H)
    assert set(GH) == set(G) | set(H)
    assert set(GH.edges(keys=True)) == set(G.edges(keys=True)) | set(H.edges(keys=True))


def test_full_join_graph():
    # Simple Graphs
    G = nx.Graph()
    G.add_node(0)
    G.add_edge(1, 2)
    H = nx.Graph()
    H.add_edge(3, 4)

    U = nx.full_join(G, H)
    assert set(U) == set(G) | set(H)
    assert len(U) == len(G) + len(H)
    assert len(U.edges()) == len(G.edges()) + len(H.edges()) + len(G) * len(H)

    # Rename
    U = nx.full_join(G, H, rename=("g", "h"))
    assert set(U) == {"g0", "g1", "g2", "h3", "h4"}
    assert len(U) == len(G) + len(H)
    assert len(U.edges()) == len(G.edges()) + len(H.edges()) + len(G) * len(H)

    # Rename graphs with string-like nodes
    G = nx.Graph()
    G.add_node("a")
    G.add_edge("b", "c")
    H = nx.Graph()
    H.add_edge("d", "e")

    U = nx.full_join(G, H, rename=("g", "h"))
    assert set(U) == {"ga", "gb", "gc", "hd", "he"}
    assert len(U) == len(G) + len(H)
    assert len(U.edges()) == len(G.edges()) + len(H.edges()) + len(G) * len(H)

    # DiGraphs
    G = nx.DiGraph()
    G.add_node(0)
    G.add_edge(1, 2)
    H = nx.DiGraph()
    H.add_edge(3, 4)

    U = nx.full_join(G, H)
    assert set(U) == set(G) | set(H)
    assert len(U) == len(G) + len(H)
    assert len(U.edges()) == len(G.edges()) + len(H.edges()) + len(G) * len(H) * 2

    # DiGraphs Rename
    U = nx.full_join(G, H, rename=("g", "h"))
    assert set(U) == {"g0", "g1", "g2", "h3", "h4"}
    assert len(U) == len(G) + len(H)
    assert len(U.edges()) == len(G.edges()) + len(H.edges()) + len(G) * len(H) * 2


def test_full_join_multigraph():
    # MultiGraphs
    G = nx.MultiGraph()
    G.add_node(0)
    G.add_edge(1, 2)
    H = nx.MultiGraph()
    H.add_edge(3, 4)

    U = nx.full_join(G, H)
    assert set(U) == set(G) | set(H)
    assert len(U) == len(G) + len(H)
    assert len(U.edges()) == len(G.edges()) + len(H.edges()) + len(G) * len(H)

    # MultiGraphs rename
    U = nx.full_join(G, H, rename=("g", "h"))
    assert set(U) == {"g0", "g1", "g2", "h3", "h4"}
    assert len(U) == len(G) + len(H)
    assert len(U.edges()) == len(G.edges()) + len(H.edges()) + len(G) * len(H)

    # MultiDiGraphs
    G = nx.MultiDiGraph()
    G.add_node(0)
    G.add_edge(1, 2)
    H = nx.MultiDiGraph()
    H.add_edge(3, 4)

    U = nx.full_join(G, H)
    assert set(U) == set(G) | set(H)
    assert len(U) == len(G) + len(H)
    assert len(U.edges()) == len(G.edges()) + len(H.edges()) + len(G) * len(H) * 2

    # MultiDiGraphs rename
    U = nx.full_join(G, H, rename=("g", "h"))
    assert set(U) == {"g0", "g1", "g2", "h3", "h4"}
    assert len(U) == len(G) + len(H)
    assert len(U.edges()) == len(G.edges()) + len(H.edges()) + len(G) * len(H) * 2


def test_mixed_type_union():
    G = nx.Graph()
    H = nx.MultiGraph()
    pytest.raises(nx.NetworkXError, nx.union, G, H)
    pytest.raises(nx.NetworkXError, nx.disjoint_union, G, H)
    pytest.raises(nx.NetworkXError, nx.intersection, G, H)
    pytest.raises(nx.NetworkXError, nx.difference, G, H)
    pytest.raises(nx.NetworkXError, nx.symmetric_difference, G, H)
    pytest.raises(nx.NetworkXError, nx.compose, G, H)


class TestRelationalCompose:
    def create_empty_g(self, with_data=False):
        return self.gclass()

    def create_empty_h(self, with_data=False):
        return self.hclass()

    def create_simple_self_g(self, with_data=False):
        G = self.create_empty_g(with_data)
        G.add_edge(2, 2, **({"size": 2**1} if with_data else {}))
        return G

    def create_multi_self_g(self, with_data=False):
        G = self.create_simple_self_g(with_data)
        G.add_edge(2, 2, **({"size": 2**2} if with_data else {}))
        return G

    def create_multi_self_g_keys(self, with_data=False):
        G = self.create_empty_g(with_data)
        G.add_edge(2, 2, "A", **({"size": 2**1} if with_data else {}))
        G.add_edge(2, 2, "B", **({"size": 2**2} if with_data else {}))
        return G

    def create_simple_forw_g(self, with_data=False):
        G = self.create_empty_g(with_data)
        G.add_edge(1, 2, **({"size": 3**1} if with_data else {}))
        return G

    def create_multi_forw_g(self, with_data=False):
        G = self.create_simple_forw_g(with_data)
        G.add_edge(1, 2, **({"size": 3**2} if with_data else {}))
        return G

    def create_multi_forw_g_keys(self, with_data=False):
        G = self.create_empty_g(with_data)
        G.add_edge(1, 2, "A", **({"size": 3**1} if with_data else {}))
        G.add_edge(1, 2, "B", **({"size": 3**2} if with_data else {}))
        return G

    def create_simple_rev_g(self, with_data=False):
        G = self.create_empty_g(with_data)
        G.add_edge(2, 1, **({"size": 3**1} if with_data else {}))
        return G

    def create_multi_rev_g(self, with_data=False):
        G = self.create_simple_rev_g(with_data)
        G.add_edge(2, 1, **({"size": 3**2} if with_data else {}))
        return G

    def create_multi_rev_g_keys(self, with_data=False):
        G = self.create_empty_g(with_data)
        G.add_edge(2, 1, "A", **({"size": 3**1} if with_data else {}))
        G.add_edge(2, 1, "B", **({"size": 3**2} if with_data else {}))
        return G

    def create_simple_h(self, with_data=False):
        H = self.create_empty_h(with_data)
        H.add_edge(2, 3, **({"size": 5**1} if with_data else {}))
        H.add_edge(2, 4, **({"size": 7**1} if with_data else {}))
        return H

    def create_multi_h(self, with_data=False):
        H = self.create_simple_h(with_data)
        H.add_edge(2, 3, **({"size": 5**2} if with_data else {}))
        H.add_edge(2, 3, **({"size": 5**3} if with_data else {}))
        return H

    def create_multi_h_keys(self, with_data=False):
        H = self.create_empty_h(with_data)
        H.add_edge(2, 3, "B", **({"size": 5**1} if with_data else {}))
        H.add_edge(2, 3, "C", **({"size": 5**2} if with_data else {}))
        H.add_edge(2, 4, **({"size": 7**1} if with_data else {}))
        return H

    leading_directed_graph_combinations = [
        (nx.DiGraph, nx.DiGraph),
        (nx.DiGraph, nx.Graph),
    ]
    leading_nondirected_graph_combinations = [
        (nx.Graph, nx.DiGraph),
        (nx.Graph, nx.Graph),
    ]
    leading_directed_multigraph_combinations = [
        (nx.MultiDiGraph, nx.MultiDiGraph),
        (nx.MultiDiGraph, nx.MultiGraph),
    ]
    leading_nondirected_multigraph_combinations = [
        (nx.MultiGraph, nx.MultiDiGraph),
        (nx.MultiGraph, nx.MultiGraph),
    ]
    leading_directed_mixed_graph_multigraph_combinations = [
        (nx.DiGraph, nx.MultiDiGraph),
        (nx.DiGraph, nx.MultiGraph),
        (nx.MultiDiGraph, nx.DiGraph),
        (nx.MultiDiGraph, nx.Graph),
    ]
    leading_nondirected_mixed_graph_multigraph_combinations = [
        (nx.Graph, nx.MultiDiGraph),
        (nx.Graph, nx.MultiGraph),
        (nx.MultiGraph, nx.DiGraph),
        (nx.MultiGraph, nx.Graph),
    ]
    leading_simple_mixed_combinations = [
        (nx.DiGraph, nx.MultiDiGraph),
        (nx.DiGraph, nx.MultiGraph),
        (nx.Graph, nx.MultiDiGraph),
        (nx.Graph, nx.MultiGraph),
    ]
    leading_multi_mixed_combinations = [
        (nx.MultiDiGraph, nx.DiGraph),
        (nx.MultiDiGraph, nx.Graph),
        (nx.MultiGraph, nx.DiGraph),
        (nx.MultiGraph, nx.Graph),
    ]
    leading_directed_graph_and_multigraph_combinations = leading_directed_graph_combinations + leading_directed_multigraph_combinations + leading_directed_mixed_graph_multigraph_combinations
    leading_nondirected_graph_and_multigraph_combinations = leading_nondirected_graph_combinations + leading_nondirected_multigraph_combinations + leading_nondirected_mixed_graph_multigraph_combinations
    all_graph_combinations = leading_directed_graph_combinations + leading_nondirected_graph_combinations
    all_multigraph_combinations = leading_nondirected_multigraph_combinations + leading_directed_multigraph_combinations
    all_graph_and_multigraph_combinations = all_graph_combinations  + all_multigraph_combinations + leading_directed_mixed_graph_multigraph_combinations + leading_nondirected_mixed_graph_multigraph_combinations

    empty_node_set = set([])
    self_g_node_set = set([2])
    edge_g_node_set = set([1, 2])
    h_node_set = set([2, 3, 4])
    self_g_h_node_set = self_g_node_set | h_node_set
    edge_g_h_node_set = edge_g_node_set | h_node_set

    empty_edge_set = set([])
    self_g_h_edge_set = set([(2, 3), (2, 4)])
    edge_g_h_edge_set = set([(1, 3), (1, 4)])
    matching_self_g_h_edge_set = set([(2, 3)])
    matching_edge_g_h_edge_set = set([(1, 3)])

    simple_g_h_edge_count = 2
    multi_g_h_edge_count = 8
    matching_multi_g_h_edge_count = 1
    default_matching_multi_g_h_edge_count = 3
    mixed_g_h_edge_count = 4

    edge_data_combiner = lambda self, gattr, hattr: {"size": gattr["size"]*hattr["size"]}


    def check_simple_self_g_h_no_edge_attribs(self, R):
        assert "size" not in R[2][3]
        assert "size" not in R[2][4]

    def check_simple_self_g_h_edge_attribs(self, R):
        assert R[2][3]["size"] == 10
        assert R[2][4]["size"] == 14

    def check_simple_edge_g_h_edge_attribs(self, R):
        assert R[1][3]["size"] == 15
        assert R[1][4]["size"] == 21

    def check_multi_self_g_h_edge_attribs(self, R):
        assert {data["size"] for data in R[2][3].values()} == set([10, 50, 250, 20, 100, 500])
        assert {data["size"] for data in R[2][4].values()} == set([14, 28])

    def check_mixed_leading_simple_self_g_h_edge_attribs(self, R):
        assert {data["size"] for data in R[2][3].values()} == set([10, 50, 250])
        assert {data["size"] for data in R[2][4].values()} == set([14])

    def check_mixed_leading_multi_self_g_h_edge_attribs(self, R):
        assert {data["size"] for data in R[2][3].values()} == set([10, 20])
        assert {data["size"] for data in R[2][4].values()} == set([14, 28])

    def check_matching_multi_self_g_h_edge_attribs(self, R):
        assert {data["size"] for data in R[2][3].values()} == set([20])
        assert 4 not in R[2]

    def check_default_matching_multi_self_g_h_edge_attribs(self, R):
        assert {data["size"] for data in R[2][3].values()} == set([10, 100])
        assert {data["size"] for data in R[2][4].values()} == set([14])

    def check_multi_edge_g_h_edge_attribs(self, R):
        assert {data["size"] for data in R[1][3].values()} == set([15, 75, 375, 45, 225, 1125])
        assert {data["size"] for data in R[1][4].values()} == set([21, 63])

    def check_matching_multi_edge_g_h_edge_attribs(self, R):
        assert {data["size"] for data in R[1][3].values()} == set([45])
        assert 4 not in R[1]

    def check_default_matching_multi_edge_g_h_edge_attribs(self, R):
        assert {data["size"] for data in R[1][3].values()} == set([15, 225])
        assert {data["size"] for data in R[1][4].values()} == set([21])


    def test_trivial_composition_empty_graphs(self):
        for self.gclass, self.hclass in self.all_graph_and_multigraph_combinations:
            R = nx.relational_compose(
                self.create_empty_g(),
                self.create_empty_h(),
            )

            assert set(R.nodes()) == TestRelationalCompose.empty_node_set
            assert set(R.edges()) == TestRelationalCompose.empty_edge_set


    def test_trivial_composition_empty_nonempty_graphs(self):
        for self.gclass, self.hclass in self.all_graph_and_multigraph_combinations:
            R = nx.relational_compose(
                self.create_empty_g(),
                self.create_simple_h(),
            )

            assert set(R.nodes()) == TestRelationalCompose.h_node_set
            assert set(R.edges()) == TestRelationalCompose.empty_edge_set


    def test_trivial_composition_self_empty_graphs(self):
        for self.gclass, self.hclass in self.all_graph_and_multigraph_combinations:
            R = nx.relational_compose(
                self.create_simple_self_g(),
                self.create_empty_h(),
            )

            assert set(R.nodes()) == TestRelationalCompose.self_g_node_set
            assert set(R.edges()) == TestRelationalCompose.empty_edge_set


    def test_trivial_composition_multi_empty_nonempty_graphs(self):
        for self.gclass, self.hclass in self.all_multigraph_combinations:
            R = nx.relational_compose(
                self.create_empty_g(),
                self.create_multi_h(),
            )

            assert set(R.nodes()) == TestRelationalCompose.h_node_set
            assert set(R.edges()) == TestRelationalCompose.empty_edge_set


    def test_trivial_composition_multi_keys_empty_nonempty_graphs(self):
        for self.gclass, self.hclass in self.all_multigraph_combinations:
            R = nx.relational_compose(
                self.create_empty_g(),
                self.create_multi_h_keys(),
                with_keys=True,
            )

            assert set(R.nodes()) == TestRelationalCompose.h_node_set
            assert set(R.edges()) == TestRelationalCompose.empty_edge_set


    def test_trivial_composition_multi_default_keys_empty_nonempty_graphs(self):
        for self.gclass, self.hclass in self.all_multigraph_combinations:
            R = nx.relational_compose(
                self.create_empty_g(),
                self.create_multi_h(),
                with_keys=True,
            )

            assert set(R.nodes()) == TestRelationalCompose.h_node_set
            assert set(R.edges()) == TestRelationalCompose.empty_edge_set


    def test_trivial_composition_multi_self_empty_graphs(self):
        for self.gclass, self.hclass in self.all_multigraph_combinations:
            R = nx.relational_compose(
                self.create_multi_self_g(),
                self.create_empty_h(),
            )

            assert set(R.nodes()) == TestRelationalCompose.self_g_node_set
            assert set(R.edges()) == TestRelationalCompose.empty_edge_set


    def test_trivial_composition_multi_keys_self_empty_graphs(self):
        for self.gclass, self.hclass in self.all_multigraph_combinations:
            R = nx.relational_compose(
                self.create_multi_self_g_keys(),
                self.create_empty_h(),
                with_keys=True,
            )

            assert set(R.nodes()) == TestRelationalCompose.self_g_node_set
            assert set(R.edges()) == TestRelationalCompose.empty_edge_set


    def test_trivial_composition_multi_default_keys_self_empty_graphs(self):
        for self.gclass, self.hclass in self.all_multigraph_combinations:
            R = nx.relational_compose(
                self.create_multi_self_g(),
                self.create_empty_h(),
                with_keys=True,
            )

            assert set(R.nodes()) == TestRelationalCompose.self_g_node_set
            assert set(R.edges()) == TestRelationalCompose.empty_edge_set


    def test_composition_self_nonempty_graphs_with_data(self):
        for self.gclass, self.hclass in self.all_graph_combinations:
            R = nx.relational_compose(
                self.create_simple_self_g(with_data=True),
                self.create_simple_h(with_data=True),
                edge_data_combiner = self.edge_data_combiner,
            )

            assert set(R.nodes()) == TestRelationalCompose.self_g_h_node_set
            assert set(R.edges()) == TestRelationalCompose.self_g_h_edge_set
            assert len(R.edges()) == TestRelationalCompose.simple_g_h_edge_count
            self.check_simple_self_g_h_edge_attribs(R)


    def test_composition_multi_self_nonempty_simple_then_multi_with_data(self):
        for self.gclass, self.hclass in self.leading_simple_mixed_combinations:
            R = nx.relational_compose(
                self.create_simple_self_g(with_data=True),
                self.create_multi_h(with_data=True),
                edge_data_combiner = self.edge_data_combiner,
            )

            assert set(R.nodes()) == TestRelationalCompose.self_g_h_node_set
            assert set(R.edges()) == TestRelationalCompose.self_g_h_edge_set
            assert len(R.edges()) == TestRelationalCompose.mixed_g_h_edge_count
            self.check_mixed_leading_simple_self_g_h_edge_attribs(R)


    def test_composition_multi_self_nonempty_multi_then_simple_with_data(self):
        for self.gclass, self.hclass in self.leading_multi_mixed_combinations:
            R = nx.relational_compose(
                self.create_multi_self_g(with_data=True),
                self.create_simple_h(with_data=True),
                edge_data_combiner = self.edge_data_combiner,
            )

            assert set(R.nodes()) == TestRelationalCompose.self_g_h_node_set
            assert set(R.edges()) == TestRelationalCompose.self_g_h_edge_set
            assert len(R.edges()) == TestRelationalCompose.mixed_g_h_edge_count
            self.check_mixed_leading_multi_self_g_h_edge_attribs(R)


    def test_composition_multi_self_nonempty_graphs_with_data(self):
        for self.gclass, self.hclass in self.all_multigraph_combinations:
            R = nx.relational_compose(
                self.create_multi_self_g(with_data=True),
                self.create_multi_h(with_data=True),
                edge_data_combiner = self.edge_data_combiner,
            )

            assert set(R.nodes()) == TestRelationalCompose.self_g_h_node_set
            assert set(R.edges()) == TestRelationalCompose.self_g_h_edge_set
            assert len(R.edges()) == TestRelationalCompose.multi_g_h_edge_count
            self.check_multi_self_g_h_edge_attribs(R)


    def test_composition_multi_keys_self_nonempty_graphs_with_data(self):
        for self.gclass, self.hclass in self.all_multigraph_combinations:
            R = nx.relational_compose(
                self.create_multi_self_g_keys(with_data=True),
                self.create_multi_h_keys(with_data=True),
                with_keys=True,
                edge_data_combiner = self.edge_data_combiner,
            )

            assert set(R.nodes()) == TestRelationalCompose.self_g_h_node_set
            assert set(R.edges()) == TestRelationalCompose.matching_self_g_h_edge_set
            assert len(R.edges()) == TestRelationalCompose.matching_multi_g_h_edge_count
            self.check_matching_multi_self_g_h_edge_attribs(R)


    def test_composition_multi_default_keys_self_nonempty_graphs_with_data(self):
        for self.gclass, self.hclass in self.all_multigraph_combinations:
            R = nx.relational_compose(
                self.create_multi_self_g(with_data=True),
                self.create_multi_h(with_data=True),
                with_keys=True,
                edge_data_combiner = self.edge_data_combiner,
            )

            assert set(R.nodes()) == TestRelationalCompose.self_g_h_node_set
            assert set(R.edges()) == TestRelationalCompose.self_g_h_edge_set
            assert len(R.edges()) == TestRelationalCompose.default_matching_multi_g_h_edge_count
            self.check_default_matching_multi_self_g_h_edge_attribs(R)


    def test_composition_forw_edge_nonempty_graphs_with_data(self):
        for self.gclass, self.hclass in self.all_graph_combinations:
            R = nx.relational_compose(
                self.create_simple_forw_g(with_data=True),
                self.create_simple_h(with_data=True),
                edge_data_combiner = self.edge_data_combiner,
            )

            assert set(R.nodes()) == TestRelationalCompose.edge_g_h_node_set
            assert set(R.edges()) == TestRelationalCompose.edge_g_h_edge_set
            assert len(R.edges()) == TestRelationalCompose.simple_g_h_edge_count
            self.check_simple_edge_g_h_edge_attribs(R)


    def test_composition_rev_edge_undirected_nonempty_graphs_with_data(self):
        for self.gclass, self.hclass in self.leading_nondirected_graph_combinations:
            R = nx.relational_compose(
                self.create_simple_rev_g(with_data=True),
                self.create_simple_h(with_data=True),
                edge_data_combiner = self.edge_data_combiner,
            )

            assert set(R.nodes()) == TestRelationalCompose.edge_g_h_node_set
            assert set(R.edges()) == TestRelationalCompose.edge_g_h_edge_set
            assert len(R.edges()) == TestRelationalCompose.simple_g_h_edge_count
            self.check_simple_edge_g_h_edge_attribs(R)


    def test_composition_multi_forw_edge_nonempty_graphs_with_data(self):
        for self.gclass, self.hclass in self.all_multigraph_combinations:
            R = nx.relational_compose(
                self.create_multi_forw_g(with_data=True),
                self.create_multi_h(with_data=True),
                edge_data_combiner = self.edge_data_combiner,
            )

            assert set(R.nodes()) == TestRelationalCompose.edge_g_h_node_set
            assert set(R.edges()) == TestRelationalCompose.edge_g_h_edge_set
            assert len(R.edges()) == TestRelationalCompose.multi_g_h_edge_count
            self.check_multi_edge_g_h_edge_attribs(R)


    def test_composition_multi_rev_edge_undirected_nonempty_graphs_with_data(self):
        for self.gclass, self.hclass in self.leading_nondirected_multigraph_combinations:
            R = nx.relational_compose(
                self.create_multi_rev_g(with_data=True),
                self.create_multi_h(with_data=True),
                edge_data_combiner = self.edge_data_combiner,
            )

            assert set(R.nodes()) == TestRelationalCompose.edge_g_h_node_set
            assert set(R.edges()) == TestRelationalCompose.edge_g_h_edge_set
            assert len(R.edges()) == TestRelationalCompose.multi_g_h_edge_count
            self.check_multi_edge_g_h_edge_attribs(R)


    def test_composition_multi_keys_forw_edge_nonempty_graphs_with_data(self):
        for self.gclass, self.hclass in self.all_multigraph_combinations:
            R = nx.relational_compose(
                self.create_multi_forw_g_keys(with_data=True),
                self.create_multi_h_keys(with_data=True),
                with_keys=True,
                edge_data_combiner = self.edge_data_combiner,
            )

            assert set(R.nodes()) == TestRelationalCompose.edge_g_h_node_set
            assert set(R.edges()) == TestRelationalCompose.matching_edge_g_h_edge_set
            assert len(R.edges()) == TestRelationalCompose.matching_multi_g_h_edge_count
            self.check_matching_multi_edge_g_h_edge_attribs(R)


    def test_composition_multi_keys_rev_edge_undirected_nonempty_graphs_with_data(self):
        for self.gclass, self.hclass in self.leading_nondirected_multigraph_combinations:
            R = nx.relational_compose(
                self.create_multi_rev_g_keys(with_data=True),
                self.create_multi_h_keys(with_data=True),
                with_keys=True,
                edge_data_combiner = self.edge_data_combiner,
            )

            assert set(R.nodes()) == TestRelationalCompose.edge_g_h_node_set
            assert set(R.edges()) == TestRelationalCompose.matching_edge_g_h_edge_set
            assert len(R.edges()) == TestRelationalCompose.matching_multi_g_h_edge_count
            self.check_matching_multi_edge_g_h_edge_attribs(R)


    def test_composition_multi_keys_default_forw_edge_nonempty_graphs_with_data(self):
        for self.gclass, self.hclass in self.all_multigraph_combinations:
            R = nx.relational_compose(
                self.create_multi_forw_g(with_data=True),
                self.create_multi_h(with_data=True),
                with_keys=True,
                edge_data_combiner=self.edge_data_combiner,
            )

            assert set(R.nodes()) == TestRelationalCompose.edge_g_h_node_set
            assert set(R.edges()) == TestRelationalCompose.edge_g_h_edge_set
            assert len(R.edges()) == TestRelationalCompose.default_matching_multi_g_h_edge_count
            self.check_default_matching_multi_edge_g_h_edge_attribs(R)


    def test_composition_multi_keys_default_rev_edge_undirected_nonempty_graphs_with_data(self):
        for self.gclass, self.hclass in self.leading_nondirected_multigraph_combinations:
            R = nx.relational_compose(
                self.create_multi_rev_g(with_data=True),
                self.create_multi_h(with_data=True),
                with_keys=True,
                edge_data_combiner = self.edge_data_combiner,
            )

            assert set(R.nodes()) == TestRelationalCompose.edge_g_h_node_set
            assert set(R.edges()) == TestRelationalCompose.edge_g_h_edge_set
            assert len(R.edges()) == TestRelationalCompose.default_matching_multi_g_h_edge_count
            self.check_default_matching_multi_edge_g_h_edge_attribs(R)


    def test_trivial_composition_rev_edge_directed_nonempty_graphs_with_data(self):
        for self.gclass, self.hclass in self.leading_directed_graph_and_multigraph_combinations:
            R = nx.relational_compose(
                self.create_simple_rev_g(with_data=True),
                self.create_simple_h(with_data=True),
                edge_data_combiner=self.edge_data_combiner,
            )

            assert set(R.nodes()) == TestRelationalCompose.edge_g_h_node_set
            assert set(R.edges()) == TestRelationalCompose.empty_edge_set


    def test_trivial_composition_multi_rev_edge_directed_nonempty_graphs_with_data(self):
        for self.gclass, self.hclass in self.leading_directed_multigraph_combinations:
            R = nx.relational_compose(
                self.create_multi_rev_g(with_data=True),
                self.create_multi_h(with_data=True),
                edge_data_combiner = self.edge_data_combiner,
            )

            assert set(R.nodes()) == TestRelationalCompose.edge_g_h_node_set
            assert set(R.edges()) == TestRelationalCompose.empty_edge_set


    def test_trivial_composition_multi_keys_rev_edge_directed_nonempty_graphs_with_data(self):
        for self.gclass, self.hclass in self.leading_directed_multigraph_combinations:
            R = nx.relational_compose(
                self.create_multi_rev_g_keys(with_data=True),
                self.create_multi_h_keys(with_data=True),
                with_keys=True,
                edge_data_combiner = self.edge_data_combiner,
            )

            assert set(R.nodes()) == TestRelationalCompose.edge_g_h_node_set
            assert set(R.edges()) == TestRelationalCompose.empty_edge_set


    def test_trivial_composition_multi_keys_default_rev_edge_directed_nonempty_graphs_with_data(self):
        for self.gclass, self.hclass in self.leading_directed_multigraph_combinations:
            R = nx.relational_compose(
                self.create_multi_rev_g(with_data=True),
                self.create_multi_h(with_data=True),
                with_keys=True,
                edge_data_combiner = self.edge_data_combiner,
            )

            assert set(R.nodes()) == TestRelationalCompose.edge_g_h_node_set
            assert set(R.edges()) == TestRelationalCompose.empty_edge_set
