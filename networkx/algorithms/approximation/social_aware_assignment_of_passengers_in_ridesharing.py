"""
Implementation of the Social Aware Assignment of Passengers in Ridesharing
Which was described in the article:
Levinger, C., Hazon, N., & Azaria, A. (2022). Social Aware Assignment of Passengers in Ridesharing.
In Proceedings of the 2022 ACM Conference on Economics and Computation (EC 2022).
Short version: http://azariaa.com/Content/Publications/Social_Assignment_SA.pdf
Full version: https://github.com/VictoKu1/ResearchAlgorithmsCourse1/blob/main/Article/2022%2C%20Chaya%20Amos%20Noam%2C%20Socially%20aware%20assignment%20of%20passengers%20in%20ride%20sharing.pdf

Paper ID: 1862

Implementation of match_and_merge
algorithm is based on the pseudocode from the article
which is written by Victor Kushnir.
"""
import networkx as nx
from networkx.utils import not_implemented_for
import logging

__all__ = ["match_and_merge"]

# Set the logger
LOG_FORMAT = "%(levelname)s, time: %(asctime)s ,line: %(lineno)d, %(message)s"
logging.basicConfig(filename="social_aware_assignment_of_passengers_in_ridesharing.log", level=logging.DEBUG,format=LOG_FORMAT)
logger = logging.getLogger()

@not_implemented_for("directed")
def match_and_merge(G: nx.Graph, k: int) -> list:
    """
    An approximation algorithm for any k ≥ 3, provides a solution for the social aware assignment problem with a ratio of 1/(k-1).

    As described in the article under the section "Algorithm 1: Match and Merge".

    Function receives a graph G and a number k, and returns a partition P of G of all matched sets.

    The algorithm consists of k - 1 rounds. Each round is composed of a matching phase followed by a merging phase.
    Specifically, in round l MnM computes a maximum matching, M_l ⊆ E_l , for G_l (where G_1 = G). In the merging phase, MnM creates a graph
    G_(l+1) that includes a unified node for each pair of matched nodes. G_(l+1) also includes all unmatched nodes, along with their
    edges to the unified nodes. Clearly, each node in V_l is composed of up-to l nodes
    from V_1. Finally, MnM returns the partition, P, of all the matched sets.

    :param G: Graph
    :param k: Number of passengers
    :return: A partition P of G of all matched sets
    
    Example where G={(v1,v2),(v2,v3),(v3,v4),(v4,v5),(v4,v6)} and k=4:
    >>> G = nx.Graph()
    >>> list_of_edges = [(1, 2), (2, 3), (3, 4), (4, 5), (4, 6)]
    >>> G.add_edges_from(list_of_edges)
    >>> k = 4
    >>> print(match_and_merge(G, k))
    [[1, 2], [3, 4, 5, 6]]
    """
    logger.info(f"match_and_merge(G={G}, k={k})")
    logger.debug("Checking for k correctness")
    # Check if k is correct
    if G.number_of_nodes() < k:
        logger.error(f"Failed a check G.number_of_nodes() ({G.number_of_nodes()}) < k ({k}), should now raise an error")
        raise nx.NetworkXError("k cannot be greater than the number of nodes in the graph G")
    # If k is negative, raise an error
    elif k < 0:
        logger.error(f"Checked for k ({k}) < 0, should now raise an error")
        raise nx.NetworkXError("k should be 0≤k≤|V(G)|")
    # If k is 0, return an empty list
    elif k == 0:
        logger.debug(f"Checked for k ({k}) == 0, should now return an empty list")
        return []
    # If k is 1, return a partition of G where each node is a list
    elif k == 1:
        logger.debug(f"Checked for k ({k}) == 1, should now return a partition of G where each node is a list")
        return [[node] for node in G.nodes()]
    # If k is 2, run the maximum matching algorithm on G and return the result
    elif k == 2:
        logger.debug(f"Checked for k ({k}) == 2, should now run the maximum matching algorithm on G and return the result")
        return [list(partition) for partition in nx.maximal_matching(G)]
    else:
        logger.debug("Should now run the algorithm")
        logger.debug("Initialization of the variables")
        # Implement G_l=(V_l,E_l) using a dictionary which contains a tuple of V_l and E_l
        G = {1: G}
        logger.debug(f"Initialized G={G}")
        # Should contain the maximal matching of G_l
        M = {}
        logger.debug(f"Initialized M={M}")
        # Loop to find the lth maximal matching and put it in G_(l+1)
        logger.debug(
            "Loop for l from 1 to (k-1) to find the lth maximal matching and put it in G_(l+1)")
        for l in range(1, k):
            logger.debug(f"Looping on l={l}")
            # Initialization of the unified nodes list
            unified_nodes = []
            logger.debug(f"Initialized unified_nodes={unified_nodes}")
            # Find the maximal matching of G_l
            M[l] = list(nx.maximal_matching(G[l]))
            logger.debug(f"Found the maximal matching of G_{l}={M[l]} and put it in M[{l}]")
            # Make sure that G_(l+1) is a empty graph (It was one of the steps of the algorithm in the article)
            G[l+1] = nx.Graph()
            logger.debug(f"Make an empty graph and put it in G[{l+1}]")
            # Put the nodes of G_l in G_(l+1)
            G[l+1].add_nodes_from(tuple(G[l].nodes()))
            logger.debug(f"Put the nodes of G_{l}={tuple(G[l].nodes())} in G[{l+1}]")
            # For every match in M_l, add a unified node to G_(l+1) so it will be used to find it when needed
            logger.debug(f"Looping on every match in M[{l}]={M[l]}")
            for match in M[l]:
                logger.debug(f"Looping on match={match}")
                # Add the match to the unified nodes dictionary, so it will be easier to find the unified nodes in each round
                unified_nodes.append(match)
                logger.debug(f"Added match={match} to unified_nodes={unified_nodes}")
                # Add a unified node to G_(l+1), which is a tuple of the nodes in the match
                G[l+1].add_node(match)
                logger.debug(f"Added a unified node={match} to G[{l+1}]")
                # Remove the nodes in the match from G_(l+1)
                G[l+1].remove_nodes_from(list(match))
                logger.debug(f"Removed the nodes in the match={match} from G[{l+1}]")
            # For every unified node in G_(l+1), add every v_q in G_(l+1) that is connected to it in G_l, add an edge between them in G_(l+1)
            logger.debug(f"Looping on every unified node in G[{l+1}] which is {unified_nodes}")
            for unified_node in unified_nodes:
                logger.debug(f"Looping on unified_node={unified_node}")
                logger.debug(f"Looping on every ununified node in G[{l+1}]")
                for v_q in G[l+1].nodes():
                    logger.debug(f"Looping on v_q={v_q}")
                    logger.debug(f"Making sure that v_q={v_q} is not unified_node={unified_node} and that there is an edge between v_q={v_q} and unified_node={unified_node} in G[{l}]")
                    if unified_node != v_q and any(specific_node != v_q and G[l].has_edge(specific_node, v_q) for specific_node in unified_node):
                        logger.debug(f"Also making sure that v_q={v_q} is not a tuple and that v_q={v_q} is not in unified_node={unified_node}")
                        if not isinstance(v_q, tuple):
                            logger.debug(f"v_q={v_q} is not a tuple")
                            logger.debug(f"Making sure that v_q={v_q} is not in unified_node={unified_node}")
                            if v_q in unified_node:
                                logger.debug(f"v_q={v_q} is in unified_node={unified_node}, so now it should continue to the next v_q")
                                continue
                            else:
                                logger.debug(f"v_q={v_q} is not in unified_node={unified_node}, so now it should add an edge between v_q={v_q} and unified_node={unified_node} in G[{l+1}]")
                                G[l+1].add_edge(unified_node, v_q)
                        elif all(specific_node in unified_node for specific_node in v_q) or all(specific_node in v_q for specific_node in unified_node):
                            logger.debug(f"v_q={v_q} is a tuple")
                            logger.debug(f"Made sure that all the nodes in v_q={v_q} are in unified_node={unified_node}")
                            logger.debug(f"Also checked that all the nodes in unified_node={unified_node} are in v_q={v_q}")
                            logger.debug(f"Now it should continue to the next v_q")
                            continue
                        else:
                            logger.debug(f"v_q={v_q} is a tuple")
                            G[l+1].add_edge(unified_node, v_q)
                            logger.debug(f"Added an edge between v_q={v_q} and unified_node={unified_node} in G[{l+1}]")
        logger.debug(f"Finished looping on l from 1 to (k-1) to find the lth maximal matching and put it in G_(l+1)")
        # Initialization of the partition P and for every unified node (which is a tuple of nodes) in G_k, add it to P
        P = [[unified_node] for unified_node in G[k].nodes()]
        logger.debug(f"Initialized P={P} and for every unified node (which is a tuple of nodes) in G[{k}]={G[k].nodes()}, added it to P")
        # For every partition in P, remove all inner tuple brackets
        logger.debug(f"Lopping on every partition in P={P}")
        for partition in P:
            logger.debug(f"Looping on partition={partition}")
            logger.debug(f"Making sure that there is a tuple in partition={partition}")
            logger.debug(f"Starting a while loop that will run until there is no tuple in partition={partition}")
            while any(isinstance(node, tuple) for node in partition):
                logger.debug(f"There is a tuple in partition={partition}")
                logger.debug(f"Looping on every node in partition={partition}")
                for node in partition:
                    logger.debug(f"Looping on node={node}")
                    logger.debug(f"Making sure that node={node} is a tuple")
                    if isinstance(node, tuple):
                        logger.debug(f"node={node} is a tuple")
                        partition.remove(node)
                        logger.debug(f"Removed node={node} from partition={partition}")
                        partition.extend(list(node))
                        logger.debug(f"Added the nodes in node={node} to partition={partition}")
                logger.debug(f"Finished looping on every node in partition={partition}")
            logger.debug(f"Finished looping on every node in partition={partition} and there is no tuple in partition={partition}")
            logger.debug(f"Sorting partition={partition}")
            partition.sort()
            logger.debug(f"Sorted partition={partition}")
        logger.debug(f"Finished looping on every partition in P={P}")
        # For every partition in P, sort it
        logger.debug(f"Sorting P={P}")
        P.sort()
        logger.debug(f"Sorted P={P}")
    # Return P
    logger.debug(f"Returning P={P}")
    return P

    