import pytest
import networkx as nx
from networkx.algorithms.approximation.social_aware_assignment_of_passengers_in_ridesharing import match_and_merge, find_matching

class test_social_aware_assignment_of_passengers_in_ridesharing:
    
    def test_1(self):
        G = nx.Graph()
        list_of_edges = [(1, 2), (2, 3), (3, 4), (4, 5), (4, 6)]
        G.add_edges_from(list_of_edges)
        k = 4
        assert match_and_merge(G,k)==[[1, 2], [3, 4, 5, 6]]