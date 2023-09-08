import networkx as nx
from networkx.utils import not_implemented_for

__all__ = [
    "tree_broadcast",
]


def update_broadcast_label(G, U, v):
    adj = [u for u in G.neighbors(v) if u in U]
    adj.sort(key=lambda u: G.nodes[u]["value"], reverse=True)
    return max([G.nodes[u]["value"] + i for i, u in enumerate(adj, start=1)])


@not_implemented_for("directed")
@not_implemented_for("multigraph")
def tree_broadcast(G):
    """
    This functions implements a linear algorithm for determining the minimum broadcast time
    on any tree. As a byproduct, it can also find a vertex which acts as the broadcast center,
    i.e., the vertex where the broadcast begins.
    """
    # Remove selfloops if necessary
    loop_nodes = nx.nodes_with_selfloops(G)
    try:
        node = next(loop_nodes)
    except StopIteration:
        pass
    else:
        G = G.copy()
        G.remove_edge(node, node)
        G.remove_edges_from((n, n) for n in loop_nodes)

    if G.number_of_nodes() == 2:
        return 1
    elif G.number_of_nodes() == 1:
        return 0

    U = {node for node in G.nodes() if G.degree(node) == 1}
    for u in U:
        G.nodes[u]["value"] = 0

    T = G.copy()
    T.remove_nodes_from(U)

    W = {node for node in T.nodes() if T.degree(node) == 1}

    for w in W:
        G.nodes[w]["value"] = G.degree[w] - 1

    while T.number_of_nodes() >= 2:
        w = min(W, key=lambda n: G.nodes[n]["value"])
        try:
            v = next(T.neighbors(w))
            print(f"Adjacent vertex of vertex {w}: {v}")
        except StopIteration:
            print(f"Vertex {v} has no adjacent vertices.")

        U.add(w)
        W.remove(w)
        T.remove_node(w)

        if T.degree(v) == 1:
            # update t(v)
            G.nodes[v]["value"] = update_broadcast_label(G, U, v)
            print(f"Updating broadcast time of vertex {v} to {G.nodes[v]['value']}")
            W.add(v)

    return update_broadcast_label(G, U, v)
