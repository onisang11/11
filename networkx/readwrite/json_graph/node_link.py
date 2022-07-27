from itertools import chain, count

import networkx as nx

__all__ = ["node_link_data", "node_link_graph"]


_attrs = dict(source="source", target="target", name="id", key="key", link="links")


def _to_tuple(x):
    """Converts lists to tuples, including nested lists.

    All other non-list inputs are passed through unmodified. This function is
    intended to be used to convert potentially nested lists from json files
    into valid nodes.

    Examples
    --------
    >>> _to_tuple([1, 2, [3, 4]])
    (1, 2, (3, 4))
    """
    if not isinstance(x, (tuple, list)):
        return x
    return tuple(map(_to_tuple, x))


def node_link_data(
    G, attrs=None, source="source", target="target", name="id", key="key", link="links"
):
    """Returns data in node-link format that is suitable for JSON serialization
    and use in Javascript documents.

    Parameters
    ----------
    G : NetworkX graph

    attrs : dict
        A dictionary that contains five keys 'source', 'target', 'name',
        'key' and 'link'.  The corresponding values provide the attribute
        names for storing NetworkX-internal graph data.  The values should
        be unique.  Default value::

            dict(source='source', target='target', name='id',
                 key='key', link='links')

        If some user-defined graph data use these attribute names as data keys,
        they may be silently dropped.

        .. deprecated:: 2.8.5

           The `attrs` keyword argument will be replaced with `source`, `target`, `name`,
           `key` and `link`. in networkx 3.???

           The values of the keywords must be unique.

    source : string
        A string that provides the 'source' attribute name for storing NetworkX-internal graph data.
    target : string
        A string that provides the 'target' attribute name for storing NetworkX-internal graph data.
    name : string
        A string that provides the 'name' attribute name for storing NetworkX-internal graph data.
    key : string
        A string that provides the 'key' attribute name for storing NetworkX-internal graph data.
    link : string
        A string that provides the 'link' attribute name for storing NetworkX-internal graph data.

    Returns
    -------
    data : dict
       A dictionary with node-link formatted data.

    Raises
    ------
    NetworkXError
        If values in attrs are not unique.

    Examples
    --------
    >>> from networkx.readwrite import json_graph
    >>> G = nx.Graph([("A", "B")])
    >>> data1 = json_graph.node_link_data(G)
    >>> H = nx.gn_graph(2)
    >>> data2 = json_graph.node_link_data(H, link="edges", source="from", target="to"})

    To serialize with json

    >>> import json
    >>> s1 = json.dumps(data1)
    >>> s2 = json.dumps(
    ...     data2, default={"link": "edges", "source": "from", "target": "to"}
    ... )

    Notes
    -----
    Graph, node, and link attributes are stored in this format.  Note that
    attribute keys will be converted to strings in order to comply with JSON.

    Attribute 'key' is only used for multigraphs.

    See Also
    --------
    node_link_graph, adjacency_data, tree_data
    """
    # ------ TODO: Remove between the lines after signature change is complete ----- #
    if attrs is not None:
        import warnings

        # TODO set the version number when feature will be removed.  3.???   (2x)
        msg = (
            "\n\nThe `attrs` keyword argument of node_link_data is deprecated\n"
            "and will be removed in networkx 3.???. It is replaced with explicit\n"
            "keyword arguments: `source`, `target`, `name`, `key` and `link`.\n"
            "To make this warning go away, and ensure usage is forward\n"
            "compatible, replace `attrs` with the keywords. "
            "For example:\n\n"
            "   >>> node_link_data(G, attrs={'target': 'foo', 'name': 'bar'})\n\n"
            "should instead be written as\n\n"
            "   >>> node_link_data(G, target='foo', name='bar')\n\n"
            "in networkx 3.???.\n"
            "The default values of the keywords will not change.\n"
        )
        warnings.warn(msg, DeprecationWarning, stacklevel=2)

        source = attrs.get("source", "source")
        target = attrs.get("target", "target")
        name = attrs.get("name", "name")
        key = attrs.get("key", "key")
        link = attrs.get("link", "links")
    # -------------------------------------------------- #
    multigraph = G.is_multigraph()

    # Allow 'key' to be omitted from attrs if the graph is not a multigraph.
    key = None if not multigraph else key
    if len({source, target, key}) < 3:
        raise nx.NetworkXError("Attribute names are not unique.")
    data = {
        "directed": G.is_directed(),
        "multigraph": multigraph,
        "graph": G.graph,
        "nodes": [dict(chain(G.nodes[n].items(), [(name, n)])) for n in G],
    }
    if multigraph:
        data[link] = [
            dict(chain(d.items(), [(source, u), (target, v), (key, k)]))
            for u, v, k, d in G.edges(keys=True, data=True)
        ]
    else:
        data[link] = [
            dict(chain(d.items(), [(source, u), (target, v)]))
            for u, v, d in G.edges(data=True)
        ]
    return data


def node_link_graph(
    data,
    directed=False,
    multigraph=True,
    attrs=None,
    source="source",
    target="target",
    name="id",
    key="key",
    link="links",
):
    """Returns graph from node-link data format.

    Parameters
    ----------
    data : dict
        node-link formatted graph data

    directed : bool
        If True, and direction not specified in data, return a directed graph.

    multigraph : bool
        If True, and multigraph not specified in data, return a multigraph.

    attrs : dict
        A dictionary that contains five keys 'source', 'target', 'name',
        'key' and 'link'.  The corresponding values provide the attribute
        names for storing NetworkX-internal graph data.  Default value:

            dict(source='source', target='target', name='id',
                key='key', link='links')

        .. deprecated:: 2.8.5

           The `attrs` keyword argument will be replaced with `source`, `target`, `name`,
           `key` and `link`. in networkx 3.???

           The values of the keywords must be unique.

    source : string
        A string that provides the 'source' attribute name for storing NetworkX-internal graph data.
    target : string
        A string that provides the 'target' attribute name for storing NetworkX-internal graph data.
    name : string
        A string that provides the 'name' attribute name for storing NetworkX-internal graph data.
    key : string
        A string that provides the 'key' attribute name for storing NetworkX-internal graph data.
    link : string
        A string that provides the 'link' attribute name for storing NetworkX-internal graph data.

    Returns
    -------
    G : NetworkX graph
        A NetworkX graph object

    Examples
    --------
    >>> from networkx.readwrite import json_graph
    >>> G = nx.Graph([("A", "B")])
    >>> data = json_graph.node_link_data(G)
    >>> H = json_graph.node_link_graph(data)

    Notes
    -----
    Attribute 'key' is only used for multigraphs.

    See Also
    --------
    node_link_data, adjacency_data, tree_data
    """
    # ------ TODO: Remove between the lines after signature change is complete ----- #
    if attrs is not None:
        import warnings

        # TODO set the version number when feature will be removed.  3.???   (2x)
        msg = (
            "\n\nThe `attrs` keyword argument of node_link_graph is deprecated\n"
            "and will be removed in networkx 3.???. It is replaced with explicit\n"
            "keyword arguments: `source`, `target`, `name`, `key` and `link`.\n"
            "To make this warning go away, and ensure usage is forward\n"
            "compatible, replace `attrs` with the keywords. "
            "For example:\n\n"
            "   >>> node_link_graph(data, attrs={'target': 'foo', 'name': 'bar'})\n\n"
            "should instead be written as\n\n"
            "   >>> node_link_graph(data, target='foo', name='bar')\n\n"
            "in networkx 3.???.\n"
            "The default values of the keywords will not change.\n"
        )
        warnings.warn(msg, DeprecationWarning, stacklevel=2)

        source = attrs["source"]
        target = attrs["target"]
        name = attrs["name"]
        key = attrs["key"]
        link = attrs["link"]
    # -------------------------------------------------- #
    multigraph = data.get("multigraph", multigraph)
    directed = data.get("directed", directed)
    if multigraph:
        graph = nx.MultiGraph()
    else:
        graph = nx.Graph()
    if directed:
        graph = graph.to_directed()

    # Allow 'key' to be omitted from attrs if the graph is not a multigraph.
    key = None if not multigraph else key
    graph.graph = data.get("graph", {})
    c = count()
    for d in data["nodes"]:
        node = _to_tuple(d.get(name, next(c)))
        nodedata = {str(k): v for k, v in d.items() if k != name}
        graph.add_node(node, **nodedata)
    for d in data[link]:
        src = tuple(d[source]) if isinstance(d[source], list) else d[source]
        tgt = tuple(d[target]) if isinstance(d[target], list) else d[target]
        if not multigraph:
            edgedata = {str(k): v for k, v in d.items() if k != source and k != target}
            graph.add_edge(src, tgt, **edgedata)
        else:
            ky = d.get(key, None)
            edgedata = {
                str(k): v
                for k, v in d.items()
                if k != source and k != target and k != key
            }
            graph.add_edge(src, tgt, ky, **edgedata)
    return graph
