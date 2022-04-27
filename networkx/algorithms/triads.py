# See https://github.com/networkx/networkx/pull/1474
# Copyright 2011 Reya Group <http://www.reyagroup.com>
# Copyright 2011 Alex Levenson <alex@isnotinvain.com>
# Copyright 2011 Diederik van Liere <diederik.vanliere@rotman.utoronto.ca>
"""Functions for analyzing triads of a graph."""
import pytest

from itertools import combinations, permutations
from collections import defaultdict
from random import sample

import networkx as nx
from networkx.utils import not_implemented_for

__all__ = [
    "triadic_census",
    "is_triad",
    "all_triplets",
    "all_triads",
    "triads_by_type",
    "triad_type",
    "random_triad",
]

#: The integer codes representing each type of triad.
#:
#: Triads that are the same up to symmetry have the same code.
TRICODES = (
    1,
    2,
    2,
    3,
    2,
    4,
    6,
    8,
    2,
    6,
    5,
    7,
    3,
    8,
    7,
    11,
    2,
    6,
    4,
    8,
    5,
    9,
    9,
    13,
    6,
    10,
    9,
    14,
    7,
    14,
    12,
    15,
    2,
    5,
    6,
    7,
    6,
    9,
    10,
    14,
    4,
    9,
    9,
    12,
    8,
    13,
    14,
    15,
    3,
    7,
    8,
    11,
    7,
    12,
    14,
    15,
    8,
    14,
    13,
    15,
    11,
    15,
    15,
    16,
)

#: The names of each type of triad. The order of the elements is
#: important: it corresponds to the tricodes given in :data:`TRICODES`.
TRIAD_NAMES = (
    "003",
    "012",
    "102",
    "021D",
    "021U",
    "021C",
    "111D",
    "111U",
    "030T",
    "030C",
    "201",
    "120D",
    "120U",
    "120C",
    "210",
    "300",
)


#: A dictionary mapping triad code to triad name.
TRICODE_TO_NAME = {i: TRIAD_NAMES[code - 1] for i, code in enumerate(TRICODES)}


def _tricode(G, v, u, w):
    """Returns the integer code of the given triad.

    This is some fancy magic that comes from Batagelj and Mrvar's paper. It
    treats each edge joining a pair of `v`, `u`, and `w` as a bit in
    the binary representation of an integer.

    """
    combos = ((v, u, 1), (u, v, 2), (v, w, 4), (w, v, 8), (u, w, 16), (w, u, 32))
    return sum(x for u, v, x in combos if v in G[u])


@not_implemented_for("undirected")
def triadic_census(G, nodelist=None):
    """Determines the triadic census of a directed graph.

    The triadic census is a count of how many of the 16 possible types of
    triads are present in a directed graph. If a list of nodes is passed, then
    only those triads are taken into account which have elements of nodelist in them.

    Parameters
    ----------
    G : digraph
       A NetworkX DiGraph
    nodelist : list
        List of nodes for which you want to calculate triadic census

    Returns
    -------
    census : dict
       Dictionary with triad type as keys and number of occurrences as values.

    Notes
    -----
    This algorithm has complexity $O(m)$ where $m$ is the number of edges in
    the graph.

    See also
    --------
    triad_graph

    References
    ----------
    .. [1] Vladimir Batagelj and Andrej Mrvar, A subquadratic triad census
        algorithm for large sparse networks with small maximum degree,
        University of Ljubljana,
        http://vlado.fmf.uni-lj.si/pub/networks/doc/triads/triads.pdf

    """
    # ignore nodelist duplicates and nodes not in G
    # TODO:?? raise error if nodelist not unique or nodes not in G
    nodelist = list(G.nbunch_iter(nodelist))
    nodeset = set(nodelist)
    N = len(G)
    Nnot = N - len(nodelist)  # can signal special counting for subset of nodes

    # create an ordering of nodes with nodelist nodes first
    m = {n: i for i, n in enumerate(nodelist)}
    if Nnot:
        # add non-nodelist nodes later in the ordering
        not_nodeset = G.nodes - nodeset
        m.update((n, i + N) for i, n in enumerate(not_nodeset))

    # build all_neighbor dicts for easy counting
    # After Python 3.8 can leave off these keys(). Speedup also using G._pred
    # nbrs = {n: G._pred[n].keys() | G._succ[n].keys() for n in G}
    nbrs = {n: G.pred[n].keys() | G.succ[n].keys() for n in G}
    dbl_nbrs = {n: G.pred[n].keys() & G.succ[n].keys() for n in G}

    if Nnot:
        sgl_nbrs = {n: G.pred[n].keys() ^ G.succ[n].keys() for n in not_nodeset}
        # find number of edges not incident to nodes in nodelist
        sgl = sum(1 for n in not_nodeset for nbr in sgl_nbrs[n] if nbr not in nodeset)
        sgl_edges_outside = sgl // 2
        dbl = sum(1 for n in not_nodeset for nbr in dbl_nbrs[n] if nbr not in nodeset)
        dbl_edges_outside = dbl // 2

    # Initialize the count for each triad to be zero.
    census = {name: 0 for name in TRIAD_NAMES}
    # Main loop over nodes
    for v in nodelist:
        vnbrs = nbrs[v]
        dbl_vnbrs = dbl_nbrs[v]
        if Nnot:
            # set up counts of edges attached to v.
            sgl_unbrs_bdy = sgl_unbrs_out = dbl_unbrs_bdy = dbl_unbrs_out = 0
        # TODO:  check for selfloops
        for u in vnbrs:
            if m[u] <= m[v]:
                continue
            unbrs = nbrs[u]
            neighbors = (vnbrs | unbrs) - {u, v}
            # Count connected triads.
            for w in neighbors:
                if m[u] < m[w] or (m[v] < m[w] < m[u] and v not in nbrs[w]):
                    code = _tricode(G, v, u, w)
                    census[TRICODE_TO_NAME[code]] += 1

            # Use a formula for dyadic triads with edge incident to v
            if u in dbl_vnbrs:
                census["102"] += N - len(neighbors) - 2
            else:
                census["012"] += N - len(neighbors) - 2

            # Count edges attached to v. Subtract later to get triads with v isolated
            # _out are (u,unbr) for unbrs outside boundary of nodeset
            # _bdy are (u,unbr) for unbrs on boundary of nodeset (get double counted)
            if Nnot and u not in nodeset:
                sgl_unbrs = sgl_nbrs[u]
                sgl_unbrs_bdy += len(sgl_unbrs & vnbrs - nodeset)
                sgl_unbrs_out += len(sgl_unbrs - vnbrs - nodeset)
                dbl_unbrs = dbl_nbrs[u]
                dbl_unbrs_bdy += len(dbl_unbrs & vnbrs - nodeset)
                dbl_unbrs_out += len(dbl_unbrs - vnbrs - nodeset)
        # if nodelist is G.nodes, skip this b/c we will find the edge later.
        if Nnot:
            # Count edges outside nodelist not connected with v (v isolated triads)
            census["012"] += sgl_edges_outside - (sgl_unbrs_out + sgl_unbrs_bdy // 2)
            census["102"] += dbl_edges_outside - (dbl_unbrs_out + dbl_unbrs_bdy // 2)

    # calculate null triads: "003"
    # null triads = total number of possible triads - all found triads
    total_triangles = (N * (N - 1) * (N - 2)) // 6
    triangles_without_nodelist = (Nnot * (Nnot - 1) * (Nnot - 2)) // 6
    total_census = total_triangles - triangles_without_nodelist
    census["003"] = total_census - sum(census.values())

    return census


def is_triad(G):
    """Returns True if the graph G is a triad, else False.

    Parameters
    ----------
    G : graph
       A NetworkX Graph

    Returns
    -------
    istriad : boolean
       Whether G is a valid triad
    """
    if isinstance(G, nx.Graph):
        if G.order() == 3 and nx.is_directed(G):
            if not any((n, n) in G.edges() for n in G.nodes()):
                return True
    return False


@not_implemented_for("undirected")
def all_triplets(G):
    """Returns a generator of all possible sets of 3 nodes in a DiGraph.

    Parameters
    ----------
    G : digraph
       A NetworkX DiGraph

    Returns
    -------
    triplets : generator of 3-tuples
       Generator of tuples of 3 nodes
    """
    triplets = combinations(G.nodes(), 3)
    return triplets


@not_implemented_for("undirected")
def all_triads(G):
    """A generator of all possible triads in G.

    Parameters
    ----------
    G : digraph
       A NetworkX DiGraph

    Returns
    -------
    all_triads : generator of DiGraphs
       Generator of triads (order-3 DiGraphs)
    """
    triplets = combinations(G.nodes(), 3)
    for triplet in triplets:
        yield G.subgraph(triplet).copy()


@not_implemented_for("undirected")
def triads_by_type(G):
    """Returns a list of all triads for each triad type in a directed graph.

    Parameters
    ----------
    G : digraph
       A NetworkX DiGraph

    Returns
    -------
    tri_by_type : dict
       Dictionary with triad types as keys and lists of triads as values.
    """
    # num_triads = o * (o - 1) * (o - 2) // 6
    # if num_triads > TRIAD_LIMIT: print(WARNING)
    all_tri = all_triads(G)
    tri_by_type = defaultdict(list)
    for triad in all_tri:
        name = triad_type(triad)
        tri_by_type[name].append(triad)
    return tri_by_type


@not_implemented_for("undirected")
def triad_type(G):
    """Returns the sociological triad type for a triad.

    Parameters
    ----------
    G : digraph
       A NetworkX DiGraph with 3 nodes

    Returns
    -------
    triad_type : str
       A string identifying the triad type

    Notes
    -----
    There can be 6 unique edges in a triad (order-3 DiGraph) (so 2^^6=64 unique
    triads given 3 nodes). These 64 triads each display exactly 1 of 16
    topologies of triads (topologies can be permuted). These topologies are
    identified by the following notation:

    {m}{a}{n}{type} (for example: 111D, 210, 102)

    Here:

    {m}     = number of mutual ties (takes 0, 1, 2, 3); a mutual tie is (0,1)
              AND (1,0)
    {a}     = number of assymmetric ties (takes 0, 1, 2, 3); an assymmetric tie
              is (0,1) BUT NOT (1,0) or vice versa
    {n}     = number of null ties (takes 0, 1, 2, 3); a null tie is NEITHER
              (0,1) NOR (1,0)
    {type}  = a letter (takes U, D, C, T) corresponding to up, down, cyclical
              and transitive. This is only used for topologies that can have
              more than one form (eg: 021D and 021U).

    References
    ----------
    .. [1] Snijders, T. (2012). "Transitivity and triads." University of
        Oxford.
        https://web.archive.org/web/20170830032057/http://www.stats.ox.ac.uk/~snijders/Trans_Triads_ha.pdf
    """
    if not is_triad(G):
        raise nx.NetworkXAlgorithmError("G is not a triad (order-3 DiGraph)")
    num_edges = len(G.edges())
    if num_edges == 0:
        return "003"
    elif num_edges == 1:
        return "012"
    elif num_edges == 2:
        e1, e2 = G.edges()
        if set(e1) == set(e2):
            return "102"
        elif e1[0] == e2[0]:
            return "021D"
        elif e1[1] == e2[1]:
            return "021U"
        elif e1[1] == e2[0] or e2[1] == e1[0]:
            return "021C"
    elif num_edges == 3:
        for (e1, e2, e3) in permutations(G.edges(), 3):
            if set(e1) == set(e2):
                if e3[0] in e1:
                    return "111U"
                # e3[1] in e1:
                return "111D"
            elif set(e1).symmetric_difference(set(e2)) == set(e3):
                if {e1[0], e2[0], e3[0]} == {e1[0], e2[0], e3[0]} == set(G.nodes()):
                    return "030C"
                # e3 == (e1[0], e2[1]) and e2 == (e1[1], e3[1]):
                return "030T"
    elif num_edges == 4:
        for (e1, e2, e3, e4) in permutations(G.edges(), 4):
            if set(e1) == set(e2):
                # identify pair of symmetric edges (which necessarily exists)
                if set(e3) == set(e4):
                    return "201"
                if {e3[0]} == {e4[0]} == set(e3).intersection(set(e4)):
                    return "120D"
                if {e3[1]} == {e4[1]} == set(e3).intersection(set(e4)):
                    return "120U"
                if e3[1] == e4[0]:
                    return "120C"
    elif num_edges == 5:
        return "210"
    elif num_edges == 6:
        return "300"


@not_implemented_for("undirected")
def random_triad(G):
    """Returns a random triad from a directed graph.

    Parameters
    ----------
    G : digraph
       A NetworkX DiGraph

    Returns
    -------
    G2 : subgraph
       A randomly selected triad (order-3 NetworkX DiGraph)
    """
    nodes = sample(list(G.nodes()), 3)
    G2 = G.subgraph(nodes)
    return G2


"""
@not_implemented_for('undirected')
def triadic_closures(G):
    '''Returns a list of order-3 subgraphs of G that are triadic closures.

    Parameters
    ----------
    G : digraph
       A NetworkX DiGraph

    Returns
    -------
    closures : list
       List of triads of G that are triadic closures
    '''
    pass


@not_implemented_for('undirected')
def focal_closures(G, attr_name):
    '''Returns a list of order-3 subgraphs of G that are focally closed.

    Parameters
    ----------
    G : digraph
       A NetworkX DiGraph
    attr_name : str
        An attribute name


    Returns
    -------
    closures : list
       List of triads of G that are focally closed on attr_name
    '''
    pass


@not_implemented_for('undirected')
def balanced_triads(G, crit_func):
    '''Returns a list of order-3 subgraphs of G that are stable.

    Parameters
    ----------
    G : digraph
       A NetworkX DiGraph
    crit_func : function
       A function that determines if a triad (order-3 digraph) is stable

    Returns
    -------
    triads : list
       List of triads in G that are stable
    '''
    pass
"""
