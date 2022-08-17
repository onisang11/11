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

        .. deprecated:: 2.8.6

           The `attrs` keyword argument will be replaced with `source`, `target`, `name`,
           `key` and `link`. in networkx 3.1

           If the `attrs` keyword and the new keywords are both used in a single function call (not recommended)
           the `attrs` keyword argument will take precedence.

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
        If the values of 'source', 'target' and 'key' are not unique.

    Examples
    --------
    >>> G = nx.Graph([("A", "B")])
    >>> data1 = nx.node_link_data(G)
    >>> data1
    {'directed': False, 'multigraph': False, 'graph': {}, 'nodes': [{'id': 'A'}, {'id': 'B'}], 'links': [{'source': 'A', 'target': 'B'}]}

    To serialize with JSON

    >>> import json
    >>> s1 = json.dumps(data1)
    >>> s1
    '{"directed": false, "multigraph": false, "graph": {}, "nodes": [{"id": "A"}, {"id": "B"}], "links": [{"source": "A", "target": "B"}]}'

    A graph can also be serialized by passing `node_link_data` as an encoder function. The two methods are equivalent.

    >>> s1 = json.dumps(G, default=nx.node_link_data)
    >>> s1
    '{"directed": false, "multigraph": false, "graph": {}, "nodes": [{"id": "A"}, {"id": "B"}], "links": [{"source": "A", "target": "B"}]}'

    The attribute names for storing NetworkX-internal graph data can
    be specified as keyword options.

    >>> H = nx.gn_graph(2)
    >>> data2 = nx.node_link_data(H, link="edges", source="from", target="to")
    >>> data2
    {'directed': True, 'multigraph': False, 'graph': {}, 'nodes': [{'id': 0}, {'id': 1}], 'edges': [{'from': 1, 'to': 0}]}

    Notes
    -----
    Graph, node, and link attributes are stored in this format.  Note that
    attribute keys will be converted to strings in order to comply with JSON.

    Attribute 'key' is only used for multigraphs.

    To use `node_link_data` in conjunction with `node_link_graph`,
    the keyword names for the attributes must match.


    See Also
    --------
    node_link_graph, adjacency_data, tree_data
    """
    # ------ TODO: Remove between the lines after signature change is complete ----- #
    if attrs is not None:
        import warnings

        msg = (
            "\n\nThe `attrs` keyword argument of node_link_data is deprecated\n"
            "and will be removed in networkx 3.1. It is replaced with explicit\n"
            "keyword arguments: `source`, `target`, `name`, `key` and `link`.\n"
            "To make this warning go away, and ensure usage is forward\n"
            "compatible, replace `attrs` with the keywords. "
            "For example:\n\n"
            "   >>> node_link_data(G, attrs={'target': 'foo', 'name': 'bar'})\n\n"
            "should instead be written as\n\n"
            "   >>> node_link_data(G, target='foo', name='bar')\n\n"
            "in networkx 3.1.\n"
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
    Useful for de-serialization from JSON.

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

        .. deprecated:: 2.8.6

           The `attrs` keyword argument will be replaced with the individual keywords: `source`, `target`, `name`,
           `key` and `link`. in networkx 3.1.

           If the `attrs` keyword and the new keywords are both used in a single function call (not recommended)
           the `attrs` keyword argument will take precedence.

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

    Create data in node-link format by converting a graph.

    >>> G = nx.Graph([('A', 'B')])
    >>> data = nx.node_link_data(G)
    >>> data
    {'directed': False, 'multigraph': False, 'graph': {}, 'nodes': [{'id': 'A'}, {'id': 'B'}], 'links': [{'source': 'A', 'target': 'B'}]}

    Revert data in node-link format to a graph.

    >>> H = nx.node_link_graph(data)
    >>> print(H.edges)
    [('A', 'B')]

    To serialize and deserialize a graph with JSON,

    >>> import json
    >>> d = json.dumps(node_link_data(G))
    >>> H = node_link_graph(json.loads(d))
    >>> print(G.edges, H.edges)
    [('A', 'B')] [('A', 'B')]


    Notes
    -----
    Attribute 'key' is only used for multigraphs.

    To use `node_link_data` in conjunction with `node_link_graph`,
    the keyword names for the attributes must match.

    See Also
    --------
    node_link_data, adjacency_data, tree_data
    """
    # ------ TODO: Remove between the lines after signature change is complete ----- #
    if attrs is not None:
        import warnings

        msg = (
            "\n\nThe `attrs` keyword argument of node_link_graph is deprecated\n"
            "and will be removed in networkx 3.1. It is replaced with explicit\n"
            "keyword arguments: `source`, `target`, `name`, `key` and `link`.\n"
            "To make this warning go away, and ensure usage is forward\n"
            "compatible, replace `attrs` with the keywords. "
            "For example:\n\n"
            "   >>> node_link_graph(data, attrs={'target': 'foo', 'name': 'bar'})\n\n"
            "should instead be written as\n\n"
            "   >>> node_link_graph(data, target='foo', name='bar')\n\n"
            "in networkx 3.1.\n"
            "The default values of the keywords will not change.\n"
        )
        warnings.warn(msg, DeprecationWarning, stacklevel=2)

        source = attrs.get("source", "source")
        target = attrs.get("target", "target")
        name = attrs.get("name", "name")
        key = attrs.get("key", "key")
        link = attrs.get("link", "links")
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
