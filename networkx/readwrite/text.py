"""
Text-based visual representations of graphs
"""

__all__ = ["forest_str", "graph_str"]


def forest_str(graph, with_labels=True, sources=None, write=None, ascii_only=False):
    """
    Creates a nice utf8 representation of a directed forest

    Parameters
    ----------
    graph : nx.DiGraph | nx.Graph
        Graph to represent (must be a tree, forest, or the empty graph)

    with_labels : bool
        If True will use the "label" attribute of a node to display if it
        exists otherwise it will use the node value itself. Defaults to True.

    sources : List
        Mainly relevant for undirected forests, specifies which nodes to list
        first. If unspecified the root nodes of each tree will be used for
        directed forests; for undirected forests this defaults to the nodes
        with the smallest degree.

    write : callable
        Function to use to write to, if None new lines are appended to
        a list and returned. If set to the `print` function, lines will
        be written to stdout as they are generated. If specified,
        this function will return None. Defaults to None.

    ascii_only : Boolean
        If True only ASCII characters are used to construct the visualization

    Returns
    -------
    str | None :
        utf8 representation of the tree / forest

    Example
    -------
    >>> graph = nx.balanced_tree(r=2, h=3, create_using=nx.DiGraph)
    >>> print(nx.forest_str(graph))
    ╙── 0
        ├─╼ 1
        │   ├─╼ 3
        │   │   ├─╼ 7
        │   │   └─╼ 8
        │   └─╼ 4
        │       ├─╼ 9
        │       └─╼ 10
        └─╼ 2
            ├─╼ 5
            │   ├─╼ 11
            │   └─╼ 12
            └─╼ 6
                ├─╼ 13
                └─╼ 14


    >>> graph = nx.balanced_tree(r=1, h=2, create_using=nx.Graph)
    >>> print(nx.forest_str(graph))
    ╙── 0
        └── 1
            └── 2

    >>> print(nx.forest_str(graph, ascii_only=True))
    +-- 0
        L-- 1
            L-- 2
    """
    import networkx as nx

    if len(graph.nodes) > 0:
        if not nx.is_forest(graph):
            raise nx.NetworkXNotImplemented("input must be a forest or the empty graph")

    return graph_str(
        graph,
        with_labels=with_labels,
        sources=sources,
        write=write,
        ascii_only=ascii_only,
    )


def graph_str(graph, with_labels=True, sources=None, write=None, ascii_only=False):
    """
    Creates a nice utf8 representation of a graph

    Parameters
    ----------
    graph : nx.DiGraph | nx.Graph
        Graph to represent

    with_labels : bool
        If True will use the "label" attribute of a node to display if it
        exists otherwise it will use the node value itself. Defaults to True.

    sources : List
        Mainly relevant for undirected forests, specifies which nodes to list
        first. If unspecified the root nodes of each tree will be used for
        directed forests; for undirected forests this defaults to the nodes
        with the smallest degree.

    write : callable
        Function to use to write to, if None new lines are appended to
        a list and returned. If set to the `print` function, lines will
        be written to stdout as they are generated. If specified,
        this function will return None. Defaults to None.

    ascii_only : Boolean
        If True only ASCII characters are used to construct the visualization

    Returns
    -------
    str | None :
        utf8 representation of the tree / forest

    Example
    -------
    >>> import networkx as nx
    >>> graph = nx.DiGraph()
    >>> graph.add_nodes_from(['a', 'b', 'c', 'd', 'e'])
    >>> graph.add_edges_from([
    >>>     ('a', 'd'),
    >>>     ('b', 'd'),
    >>>     ('c', 'd'),
    >>>     ('d', 'e'),
    >>>     ('f1', 'g'),
    >>>     ('f2', 'g'),
    >>> ])
    >>> nx.graph_str(graph, write=print)
    >>> graph = nx.balanced_tree(r=2, h=3, create_using=nx.DiGraph)
    >>> # A simple forest
    >>> print(nx.graph_str(graph))
    ╙── 0
        ├─╼ 1
        │   ├─╼ 3
        │   │   ├─╼ 7
        │   │   └─╼ 8
        │   └─╼ 4
        │       ├─╼ 9
        │       └─╼ 10
        └─╼ 2
            ├─╼ 5
            │   ├─╼ 11
            │   └─╼ 12
            └─╼ 6
                ├─╼ 13
                └─╼ 14

    >>> # Add a non-forest edge
    >>> graph.add_edges_from([
    >>>     (7, 1)
    >>> ])
    >>> print(nx.graph_str(graph))
    ╙── 0
        ├─╼ 1 ╾ 7
        │   ├─╼ 3
        │   │   ├─╼ 7
        │   │   │   └─╼  ...
        │   │   └─╼ 8
        │   └─╼ 4
        │       ├─╼ 9
        │       └─╼ 10
        └─╼ 2
            ├─╼ 5
            │   ├─╼ 11
            │   └─╼ 12
            └─╼ 6
                ├─╼ 13
                └─╼ 14

    >>> # A clique graph
    >>> graph = nx.erdos_renyi_graph(5, 1.0)
    >>> print(nx.graph_str(graph))
    ╙── 0
        ├── 1
        │   ├── 2 ─ 0
        │   │   ├── 3 ─ 0, 1
        │   │   │   └── 4 ─ 0, 1, 2
    """
    import networkx as nx

    printbuf = []
    if write is None:
        _write = printbuf.append
    else:
        _write = write

    # Define glphys
    # Notes on available box and arrow characters
    # https://en.wikipedia.org/wiki/Box-drawing_character
    # https://stackoverflow.com/questions/2701192/triangle-arrow
    if ascii_only:
        glyph_empty = "+"
        glyph_newtree_last = "+-- "
        glyph_newtree_mid = "+-- "
        glyph_endof_forest = "    "
        glyph_within_forest = ":   "
        glyph_within_tree = "|   "

        glyph_directed_last = "L-> "
        glyph_directed_mid = "|-> "
        glyph_directed_backedge = "<-"

        glyph_undirected_last = "L-- "
        glyph_undirected_mid = "|-- "
        glyph_undirected_backedge = "-"
    else:
        glyph_empty = "╙"
        glyph_newtree_last = "╙── "
        glyph_newtree_mid = "╟── "
        glyph_endof_forest = "    "
        glyph_within_forest = "╎   "
        glyph_within_tree = "│   "

        glyph_directed_last = "└─╼ "
        glyph_directed_mid = "├─╼ "
        glyph_directed_backedge = "╾"

        glyph_undirected_last = "└── "
        glyph_undirected_mid = "├── "
        glyph_undirected_backedge = "─"

    if len(graph.nodes) == 0:
        _write(glyph_empty)
    else:
        is_directed = graph.is_directed()
        if is_directed:
            glyph_last = glyph_directed_last
            glyph_mid = glyph_directed_mid
            glyph_backedge = glyph_directed_backedge
            succ = graph.succ
            pred = graph.pred
        else:
            glyph_last = glyph_undirected_last
            glyph_mid = glyph_undirected_mid
            glyph_backedge = glyph_undirected_backedge
            succ = graph.adj
            pred = graph.adj

        if sources is None:
            # For each connected part of the graph, choose at least
            # one node as a starting point, preferably without a parent
            if is_directed:
                sources = [
                    min(cc, key=lambda n: graph.degree[n])
                    for cc in nx.strongly_connected_components(graph)
                ]
            else:
                sources = [
                    min(cc, key=lambda n: graph.degree[n])
                    for cc in nx.connected_components(graph)
                ]

        # Populate the stack with each source node, empty indentation, and mark
        # the final node. Reverse the stack so sources are popped in the
        # correct order.
        last_idx = len(sources) - 1
        stack = [
            (None, node, "", (idx == last_idx)) for idx, node in enumerate(sources)
        ][::-1]

        seen_nodes = set()
        seen_edges = set()
        implicit_seen = set()
        while stack:
            parent, node, indent, this_islast = stack.pop()
            edge = (parent, node)

            if node is not Ellipsis:
                if node in seen_nodes:
                    continue
                seen_nodes.add(node)
                seen_edges.add(edge)

            if not indent:
                # Top level items (i.e. trees in the forest) get different
                # glyphs to indicate they are not actually connected
                if this_islast:
                    this_prefix = indent + glyph_newtree_last
                    next_prefix = indent + glyph_endof_forest
                else:
                    this_prefix = indent + glyph_newtree_mid
                    next_prefix = indent + glyph_within_forest

            else:
                # For individual tree edges distinguish between directed and
                # undirected cases
                if this_islast:
                    this_prefix = indent + glyph_last
                    next_prefix = indent + glyph_endof_forest
                else:
                    this_prefix = indent + glyph_mid
                    next_prefix = indent + glyph_within_tree

            if node is Ellipsis:
                label = " ..."
                children = []
            else:
                if with_labels:
                    label = graph.nodes[node].get("label", node)
                else:
                    label = node
                children = [child for child in succ[node] if child not in seen_nodes]
                neighbors = set(pred[node])
                others = (neighbors - set(children)) - {parent}
                implicit_seen.update(others)
                in_edges = [(node, other) for other in others]
                if in_edges:
                    in_nodes = ", ".join([str(uv[1]) for uv in in_edges])
                    suffix = " ".join(["", glyph_backedge, in_nodes])
                else:
                    suffix = ""

            _write(this_prefix + str(label) + suffix)

            # Push children on the stack in reverse order so they are popped in
            # the original order.
            idx = 1
            for idx, child in enumerate(children[::-1], start=1):
                next_islast = idx <= 1
                try_frame = (node, child, next_prefix, next_islast)
                stack.append(try_frame)

            if node in implicit_seen:
                # if have used this node in any previous implicit edges, then
                # write an outgoing "implicit" connection.
                next_islast = idx <= 1
                try_frame = (node, Ellipsis, next_prefix, next_islast)
                stack.append(try_frame)

    if write is None:
        # Only return a string if the custom write function was not specified
        return "\n".join(printbuf)
