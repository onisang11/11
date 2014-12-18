#!/usr/bin/env python
from nose.tools import *
import networkx
from test_graph import TestGraph
from test_digraph import TestDiGraph
from test_multigraph import TestMultiGraph
from test_multidigraph import TestMultiDiGraph
from collections import OrderedDict


class SpecialGraphTester(TestGraph):
    def setUp(self):
        TestGraph.setUp(self)
        self.Graph=networkx.SpecialGraph

class OrderedGraphTester(TestGraph):
    def setUp(self):
        TestGraph.setUp(self)
        def graph_factory(data,**attr):
            g=networkx.SpecialGraph(data,node_dict_factory=OrderedDict,
                    adjlist_dict_factory=OrderedDict,
                    edge_attr_dict_factory=OrderedDict,**attr)
            return g
        self.Graph=graph_factory

class ThinGraphTester(TestGraph):
    def setUp(self):
        all_edge_dict = {'weight' : 1}
        def graph_factory(data,**attr):
            g=networkx.SpecialGraph(data,
                    edge_attr_dict_factory=lambda :all_edge_dict,**attr)
            return g
        self.Graph=graph_factory
        # build dict-of-dict-of-dict K3
        ed1,ed2,ed3 = (all_edge_dict,all_edge_dict,all_edge_dict)
        self.k3adj={0: {1: ed1, 2: ed2},
                    1: {0: ed1, 2: ed3},
                    2: {0: ed2, 1: ed3}}
        self.k3edges=[(0, 1), (0, 2), (1, 2)]
        self.k3nodes=[0, 1, 2]
        self.K3=self.Graph()
        self.K3.adj=self.K3.edge=self.k3adj
        self.K3.node={}
        self.K3.node[0]={}
        self.K3.node[1]={}
        self.K3.node[2]={}




class SpecialDiGraphTester(TestDiGraph):
    def setUp(self):
        TestDiGraph.setUp(self)
        self.Graph=networkx.SpecialDiGraph

class OrderedDiGraphTester(TestDiGraph):
    def setUp(self):
        TestGraph.setUp(self)
        def graph_factory(data,**attr):
            g=networkx.SpecialDiGraph(data,node_dict_factory=OrderedDict,
                    adjlist_dict_factory=OrderedDict,
                    edge_attr_dict_factory=OrderedDict,**attr)
            return g
        self.Graph=graph_factory

class ThinDiGraphTester(TestDiGraph):
    def setUp(self):
        all_edge_dict = {'weight' : 1}
        def graph_factory(data,**attr):
            g=networkx.SpecialDiGraph(data,
                    edge_attr_dict_factory=lambda :all_edge_dict,**attr)
            return g
        self.Graph=graph_factory
        # build dict-of-dict-of-dict K3
        ed1,ed2,ed3 = (all_edge_dict,all_edge_dict,all_edge_dict)
        self.k3adj={0: {1: ed1, 2: ed2},
                    1: {0: ed1, 2: ed3},
                    2: {0: ed2, 1: ed3}}
        self.k3edges=[(0, 1), (0, 2), (1, 2)]
        self.k3nodes=[0, 1, 2]
        self.K3=self.Graph()
        self.K3.adj=self.K3.edge=self.k3adj
        self.K3.node={}
        self.K3.node[0]={}
        self.K3.node[1]={}
        self.K3.node[2]={}



class SpecialMultiGraphTester(TestMultiGraph):
    def setUp(self):
        TestMultiGraph.setUp(self)
        self.Graph=networkx.SpecialMultiGraph

class OrderedMultiGraphTester(TestMultiGraph):
    def setUp(self):
        TestMultiGraph.setUp(self)
        def graph_factory(data,**attr):
            g=networkx.SpecialMultiGraph(data,node_dict_factory=OrderedDict,
                    adjlist_dict_factory=OrderedDict,
                    edge_key_dict_factory=OrderedDict,
                    edge_attr_dict_factory=OrderedDict,**attr)
            return g
        self.Graph=graph_factory


class SpecialMultiDiGraphTester(TestMultiDiGraph):
    def setUp(self):
        TestMultiDiGraph.setUp(self)
        self.Graph=networkx.SpecialMultiDiGraph

class OrderedMultiDiGraphTester(TestMultiDiGraph):
    def setUp(self):
        TestMultiDiGraph.setUp(self)
        def graph_factory(data,**attr):
            g=networkx.SpecialMultiDiGraph(data,node_dict_factory=OrderedDict,
                    adjlist_dict_factory=OrderedDict,
                    edge_key_dict_factory=OrderedDict,
                    edge_attr_dict_factory=OrderedDict,**attr)
            return g
        self.Graph=graph_factory

