"""Basic algorithms for breadth-first searching the nodes of a graph."""
import math
from collections import deque

import networkx as nx

__all__ = [
    "bfs_edges",
    "bfs_tree",
    "bfs_predecessors",
    "bfs_successors",
    "descendants_at_distance",
    "bfs_layers",
    "bfs_labeled_edges",
]


def generic_bfs_edges(G, source, neighbors=None, depth_limit=None, sort_neighbors=None):
    """Iterate over edges in a breadth-first search.

    The breadth-first search begins at `source` and enqueues the
    neighbors of newly visited nodes specified by the `neighbors`
    function.

    Parameters
    ----------
    G : NetworkX graph

    source : node
        Starting node for the breadth-first search; this function
        iterates over only those edges in the component reachable from
        this node.

    neighbors : function
        A function that takes a newly visited node of the graph as input
        and returns an *iterator* (not just a list) of nodes that are
        neighbors of that node. If not specified, this is just the
        ``G.neighbors`` method, but in general it can be any function
        that returns an iterator over some or all of the neighbors of a
        given node, in any order.

    depth_limit : int, optional(default=len(G))
        Specify the maximum search depth

    sort_neighbors : function
        A function that takes the list of neighbors of given node as input, and
        returns an *iterator* over these neighbors but with custom ordering.

    Yields
    ------
    edge
        Edges in the breadth-first search starting from `source`.

    Examples
    --------
    >>> G = nx.path_graph(3)
    >>> print(list(nx.bfs_edges(G, 0)))
    [(0, 1), (1, 2)]
    >>> print(list(nx.bfs_edges(G, source=0, depth_limit=1)))
    [(0, 1)]

    Notes
    -----
    This implementation is from `PADS`_, which was in the public domain
    when it was first accessed in July, 2004.  The modifications
    to allow depth limits are based on the Wikipedia article
    "`Depth-limited-search`_".

    .. _PADS: http://www.ics.uci.edu/~eppstein/PADS/BFS.py
    .. _Depth-limited-search: https://en.wikipedia.org/wiki/Depth-limited_search
    """
    if callable(sort_neighbors):
        _neighbors = neighbors
        neighbors = lambda node: iter(sort_neighbors(_neighbors(node)))

    visited = {source}
    if depth_limit is None:
        depth_limit = len(G)
    queue = deque([(source, depth_limit, neighbors(source))])
    while queue:
        parent, depth_now, children = queue[0]
        try:
            child = next(children)
            if child not in visited:
                yield parent, child
                visited.add(child)
                if depth_now > 1:
                    queue.append((child, depth_now - 1, neighbors(child)))
        except StopIteration:
            queue.popleft()


@nx._dispatch
def bfs_edges(G, source, reverse=False, depth_limit=None, sort_neighbors=None):
    """Iterate over edges in a breadth-first-search starting at source.

    Parameters
    ----------
    G : NetworkX graph

    source : node
       Specify starting node for breadth-first search; this function
       iterates over only those edges in the component reachable from
       this node.

    reverse : bool, optional
       If True traverse a directed graph in the reverse direction

    depth_limit : int, optional(default=len(G))
        Specify the maximum search depth

    sort_neighbors : function
        A function that takes the list of neighbors of given node as input, and
        returns an *iterator* over these neighbors but with custom ordering.

    Yields
    ------
    edge: 2-tuple of nodes
       Yields edges resulting from the breadth-first search.

    Examples
    --------
    To get the edges in a breadth-first search::

        >>> G = nx.path_graph(3)
        >>> list(nx.bfs_edges(G, 0))
        [(0, 1), (1, 2)]
        >>> list(nx.bfs_edges(G, source=0, depth_limit=1))
        [(0, 1)]

    To get the nodes in a breadth-first search order::

        >>> G = nx.path_graph(3)
        >>> root = 2
        >>> edges = nx.bfs_edges(G, root)
        >>> nodes = [root] + [v for u, v in edges]
        >>> nodes
        [2, 1, 0]

    Notes
    -----
    The naming of this function is very similar to
    :func:`~networkx.algorithms.traversal.edgebfs.edge_bfs`. The difference
    is that ``edge_bfs`` yields edges even if they extend back to an already
    explored node while this generator yields the edges of the tree that results
    from a breadth-first-search (BFS) so no edges are reported if they extend
    to already explored nodes. That means ``edge_bfs`` reports all edges while
    ``bfs_edges`` only reports those traversed by a node-based BFS. Yet another
    description is that ``bfs_edges`` reports the edges traversed during BFS
    while ``edge_bfs`` reports all edges in the order they are explored.

    Based on the breadth-first search implementation in PADS [1]_
    by D. Eppstein, July 2004; with modifications to allow depth limits
    as described in [2]_.

    References
    ----------
    .. [1] http://www.ics.uci.edu/~eppstein/PADS/BFS.py.
    .. [2] https://en.wikipedia.org/wiki/Depth-limited_search

    See Also
    --------
    bfs_tree
    :func:`~networkx.algorithms.traversal.depth_first_search.dfs_edges`
    :func:`~networkx.algorithms.traversal.edgebfs.edge_bfs`

    """
    if reverse and G.is_directed():
        successors = G.predecessors
    else:
        successors = G.neighbors
    yield from generic_bfs_edges(G, source, successors, depth_limit, sort_neighbors)


def bfs_tree(G, source, reverse=False, depth_limit=None, sort_neighbors=None):
    """Returns an oriented tree constructed from of a breadth-first-search
    starting at source.

    Parameters
    ----------
    G : NetworkX graph

    source : node
       Specify starting node for breadth-first search

    reverse : bool, optional
       If True traverse a directed graph in the reverse direction

    depth_limit : int, optional(default=len(G))
        Specify the maximum search depth

    sort_neighbors : function
        A function that takes the list of neighbors of given node as input, and
        returns an *iterator* over these neighbors but with custom ordering.

    Returns
    -------
    T: NetworkX DiGraph
       An oriented tree

    Examples
    --------
    >>> G = nx.path_graph(3)
    >>> print(list(nx.bfs_tree(G, 1).edges()))
    [(1, 0), (1, 2)]
    >>> H = nx.Graph()
    >>> nx.add_path(H, [0, 1, 2, 3, 4, 5, 6])
    >>> nx.add_path(H, [2, 7, 8, 9, 10])
    >>> print(sorted(list(nx.bfs_tree(H, source=3, depth_limit=3).edges())))
    [(1, 0), (2, 1), (2, 7), (3, 2), (3, 4), (4, 5), (5, 6), (7, 8)]


    Notes
    -----
    Based on http://www.ics.uci.edu/~eppstein/PADS/BFS.py
    by D. Eppstein, July 2004. The modifications
    to allow depth limits based on the Wikipedia article
    "`Depth-limited-search`_".

    .. _Depth-limited-search: https://en.wikipedia.org/wiki/Depth-limited_search

    See Also
    --------
    dfs_tree
    bfs_edges
    edge_bfs
    """
    T = nx.DiGraph()
    T.add_node(source)
    edges_gen = bfs_edges(
        G,
        source,
        reverse=reverse,
        depth_limit=depth_limit,
        sort_neighbors=sort_neighbors,
    )
    T.add_edges_from(edges_gen)
    return T


@nx._dispatch
def bfs_predecessors(G, source, depth_limit=None, sort_neighbors=None):
    """Returns an iterator of predecessors in breadth-first-search from source.

    Parameters
    ----------
    G : NetworkX graph

    source : node
       Specify starting node for breadth-first search

    depth_limit : int, optional(default=len(G))
        Specify the maximum search depth

    sort_neighbors : function
        A function that takes the list of neighbors of given node as input, and
        returns an *iterator* over these neighbors but with custom ordering.

    Returns
    -------
    pred: iterator
        (node, predecessor) iterator where `predecessor` is the predecessor of
        `node` in a breadth first search starting from `source`.

    Examples
    --------
    >>> G = nx.path_graph(3)
    >>> print(dict(nx.bfs_predecessors(G, 0)))
    {1: 0, 2: 1}
    >>> H = nx.Graph()
    >>> H.add_edges_from([(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)])
    >>> print(dict(nx.bfs_predecessors(H, 0)))
    {1: 0, 2: 0, 3: 1, 4: 1, 5: 2, 6: 2}
    >>> M = nx.Graph()
    >>> nx.add_path(M, [0, 1, 2, 3, 4, 5, 6])
    >>> nx.add_path(M, [2, 7, 8, 9, 10])
    >>> print(sorted(nx.bfs_predecessors(M, source=1, depth_limit=3)))
    [(0, 1), (2, 1), (3, 2), (4, 3), (7, 2), (8, 7)]
    >>> N = nx.DiGraph()
    >>> nx.add_path(N, [0, 1, 2, 3, 4, 7])
    >>> nx.add_path(N, [3, 5, 6, 7])
    >>> print(sorted(nx.bfs_predecessors(N, source=2)))
    [(3, 2), (4, 3), (5, 3), (6, 5), (7, 4)]

    Notes
    -----
    Based on http://www.ics.uci.edu/~eppstein/PADS/BFS.py
    by D. Eppstein, July 2004. The modifications
    to allow depth limits based on the Wikipedia article
    "`Depth-limited-search`_".

    .. _Depth-limited-search: https://en.wikipedia.org/wiki/Depth-limited_search

    See Also
    --------
    bfs_tree
    bfs_edges
    edge_bfs
    """
    for s, t in bfs_edges(
        G, source, depth_limit=depth_limit, sort_neighbors=sort_neighbors
    ):
        yield (t, s)


@nx._dispatch
def bfs_successors(G, source, depth_limit=None, sort_neighbors=None):
    """Returns an iterator of successors in breadth-first-search from source.

    Parameters
    ----------
    G : NetworkX graph

    source : node
       Specify starting node for breadth-first search

    depth_limit : int, optional(default=len(G))
        Specify the maximum search depth

    sort_neighbors : function
        A function that takes the list of neighbors of given node as input, and
        returns an *iterator* over these neighbors but with custom ordering.

    Returns
    -------
    succ: iterator
       (node, successors) iterator where `successors` is the non-empty list of
       successors of `node` in a breadth first search from `source`.
       To appear in the iterator, `node` must have successors.

    Examples
    --------
    >>> G = nx.path_graph(3)
    >>> print(dict(nx.bfs_successors(G, 0)))
    {0: [1], 1: [2]}
    >>> H = nx.Graph()
    >>> H.add_edges_from([(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)])
    >>> print(dict(nx.bfs_successors(H, 0)))
    {0: [1, 2], 1: [3, 4], 2: [5, 6]}
    >>> G = nx.Graph()
    >>> nx.add_path(G, [0, 1, 2, 3, 4, 5, 6])
    >>> nx.add_path(G, [2, 7, 8, 9, 10])
    >>> print(dict(nx.bfs_successors(G, source=1, depth_limit=3)))
    {1: [0, 2], 2: [3, 7], 3: [4], 7: [8]}
    >>> G = nx.DiGraph()
    >>> nx.add_path(G, [0, 1, 2, 3, 4, 5])
    >>> print(dict(nx.bfs_successors(G, source=3)))
    {3: [4], 4: [5]}

    Notes
    -----
    Based on http://www.ics.uci.edu/~eppstein/PADS/BFS.py
    by D. Eppstein, July 2004.The modifications
    to allow depth limits based on the Wikipedia article
    "`Depth-limited-search`_".

    .. _Depth-limited-search: https://en.wikipedia.org/wiki/Depth-limited_search

    See Also
    --------
    bfs_tree
    bfs_edges
    edge_bfs
    """
    parent = source
    children = []
    for p, c in bfs_edges(
        G, source, depth_limit=depth_limit, sort_neighbors=sort_neighbors
    ):
        if p == parent:
            children.append(c)
            continue
        yield (parent, children)
        children = [c]
        parent = p
    yield (parent, children)


@nx._dispatch
def bfs_layers(G, sources):
    """Returns an iterator of all the layers in breadth-first search traversal.

    Parameters
    ----------
    G : NetworkX graph
        A graph over which to find the layers using breadth-first search.

    sources : node in `G` or list of nodes in `G`
        Specify starting nodes for single source or multiple sources breadth-first search

    Yields
    ------
    layer: list of nodes
        Yields list of nodes at the same distance from sources

    Examples
    --------
    >>> G = nx.path_graph(5)
    >>> dict(enumerate(nx.bfs_layers(G, [0, 4])))
    {0: [0, 4], 1: [1, 3], 2: [2]}
    >>> H = nx.Graph()
    >>> H.add_edges_from([(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)])
    >>> dict(enumerate(nx.bfs_layers(H, [1])))
    {0: [1], 1: [0, 3, 4], 2: [2], 3: [5, 6]}
    >>> dict(enumerate(nx.bfs_layers(H, [1, 6])))
    {0: [1, 6], 1: [0, 3, 4, 2], 2: [5]}
    """
    if sources in G:
        sources = [sources]

    current_layer = list(sources)
    visited = set(sources)

    for source in current_layer:
        if source not in G:
            raise nx.NetworkXError(f"The node {source} is not in the graph.")

    # this is basically BFS, except that the current layer only stores the nodes at
    # same distance from sources at each iteration
    while current_layer:
        yield current_layer
        next_layer = []
        for node in current_layer:
            for child in G[node]:
                if child not in visited:
                    visited.add(child)
                    next_layer.append(child)
        current_layer = next_layer


REVERSE_EDGE = "reverse"
TREE_EDGE = "tree"
FORWARD_EDGE = "forward"
LEVEL_EDGE = "level"


def bfs_labeled_edges(G, sources):
    """Iterate over edges in a breadth-first search (BFS) labeled by type.

    We generate triple of the form (*u*, *v*, *d*), where (*u*, *v*) is the
    edge being explored in the breadth-first search and *d* is one of the
    strings 'tree', 'forward', 'level', or 'reverse'.  A 'tree' edge is one in
    which *v* is first discovered and placed into the layer below *u*.  A
    'forward' edge is one in which *u* is on the layer above *v* and *v* has
    already been discovered.  A 'level' edge is one in which both *u* and *v*
    occur on the same layer.  A 'reverse' edge is one in which *u* is on a layer
    below *v*.

    We emit each edge exactly once.  In an undirected graph, 'reverse' edges do
    not occur, because each is discovered either as a 'tree' or 'forward' edge.

    Parameters
    ----------
    G : NetworkX graph
        A graph over which to find the layers using breadth-first search.

    sources : node in `G` or list of nodes in `G`
        Starting nodes for single source or multiple sources breadth-first search

    Yields
    ------
    edges: generator
       A generator of triples (*u*, *v*, *d*) where (*u*, *v*) is the edge being
       explored and *d* is described above.

    Examples
    --------
    >>> G = nx.cycle_graph(4, create_using = nx.DiGraph)
    >>> list(nx.bfs_labeled_edges(G, 0))
    [(0, 1, 'tree'), (1, 2, 'tree'), (2, 3, 'tree'), (3, 0, 'reverse')]
    >>> G = nx.complete_graph(3)
    >>> list(nx.bfs_labeled_edges(G, 0))
    [(0, 2, 'tree'), (0, 1, 'tree'), (2, 1, 'level')]
    >>> list(nx.bfs_labeled_edges(G, [0, 1]))
    [(1, 0, 'level'), (0, 2, 'tree'), (1, 2, 'forward')]
    """
    if G.is_directed():
        yield from _directed_bfs_labeled_edges(G, sources)
    else:
        yield from _undirected_bfs_labeled_edges(G, sources)


def _undirected_bfs_labeled_edges(G, sources):
    if sources in G:
        sources = [sources]

    depth = {s: 0 for s in sources}
    visited = set()
    queue = deque(depth.items())
    while queue:
        u, du = queue.popleft()
        visited.add(u)
        for v in G[u]:
            dv = depth.get(v)
            if dv is None:
                depth[v] = dv = du + 1
                queue.append((v, dv))
                yield u, v, TREE_EDGE
            else:
                if du == dv:
                    # could use either "in" or "not in" -- this emits self-loops
                    if v in visited:
                        yield u, v, LEVEL_EDGE
                elif du < dv:
                    yield u, v, FORWARD_EDGE


def _directed_bfs_labeled_edges(G, sources):
    if sources in G:
        sources = [sources]

    depth = {s: 0 for s in sources}
    queue = deque(depth.items())
    while queue:
        u, du = queue.popleft()
        for v in G[u]:
            dv = depth.get(v)
            if dv is None:
                depth[v] = dv = du + 1
                queue.append((v, dv))
                yield u, v, TREE_EDGE
            elif du < dv:
                yield u, v, FORWARD_EDGE
            elif du > dv:
                yield u, v, REVERSE_EDGE
            else:
                yield u, v, LEVEL_EDGE


@nx._dispatch
def descendants_at_distance(G, source, distance):
    """Returns all nodes at a fixed `distance` from `source` in `G`.

    Parameters
    ----------
    G : NetworkX graph
        A graph
    source : node in `G`
    distance : the distance of the wanted nodes from `source`

    Returns
    -------
    set()
        The descendants of `source` in `G` at the given `distance` from `source`

    Examples
    --------
    >>> G = nx.path_graph(5)
    >>> nx.descendants_at_distance(G, 2, 2)
    {0, 4}
    >>> H = nx.DiGraph()
    >>> H.add_edges_from([(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)])
    >>> nx.descendants_at_distance(H, 0, 2)
    {3, 4, 5, 6}
    >>> nx.descendants_at_distance(H, 5, 0)
    {5}
    >>> nx.descendants_at_distance(H, 5, 1)
    set()
    """
    if source not in G:
        raise nx.NetworkXError(f"The node {source} is not in the graph.")

    bfs_generator = nx.bfs_layers(G, source)
    for i, layer in enumerate(bfs_generator):
        if i == distance:
            return set(layer)
    return set()
