# -*- coding: utf-8 -*-
"""
Algorithm to find a minimum dominating set.

"""
#    Peng Feifei <pengff@ios.ac.cn>
#    All rights reserved.
#    BSD license.

import networkx as nx
import operator
from itertools import chain, combinations
__author__ = """Peng Feifei (pengff@ios.ac.cn)"""
__all__ = ['minimum_dominating_set','minimum_dominating']
def minimum_dominating_set(G):
	r"""Finds a minimum dominating set for undirected G. 

    A dominating set for a graph G = (V, E) is a subset D of V such that every
    vertex not in D is joined to at least one member of D by some edge. The
    domination number gamma(G) is the number of vertices in a smallest dominating
    set for G. Given a graph G = (V, E) find a minimum weight dominating set V'.

    http://en.wikipedia.org/wiki/Dominating_set

    Parameters
    ----------
    G : NetworkX graph
        Undirected graph

    Returns
    -------
    dset: List
        The minimum dominating set for graph G

    Notes
    -----
    This algorithm computes an exact minimum dominating set
    for the graph G. Runtime of the algorithm is `O(1.93782^|V|)`.

    References
    ----------
    .. [1] Fomin, Fedor V., Dieter Kratsch, and Gerhard J. Woeginger. 
           "Exact (exponential) algorithms for the dominating set problem." 
           Graph-Theoretic Concepts in Computer Science. Springer Berlin Heidelberg, 2005.
    """
	x=G.nodes()
	dset=[]
	minimum_dominating(G,x,dset)
	return dset


def minimum_dominating(G,x,dset):
    smalldegree=[]
    if len(G.nodes())==0:
    	return dset
    for i in G.nodes():
    	if G.degree(i)<3:
    		smalldegree.append(i)
    # test all possible with up to 3*|V|/8 to find a minimun dominating set
    if smalldegree==[]:
    	length=3*len(G.nodes())/8
    	for i in range(1,length+1):
    		subsets=map(list, combinations(set(G.nodes()), i))
    		for subset in subsets:
    			neighbors=set()
    			for item in subset:
    				neighbors=neighbors|set([item])
    				neighbors=neighbors|set(G.neighbors(item))
    			if list(neighbors)==G.nodes():
    				for i in subset:
    					dset.append(i)
    				break
    		break       
    	return dset
    #branch into subcases and to remove all vertices of degree one and two.
    else:
        #getting a sorted list of nodes by degree, and pick up a vertex with smallest degree.
    	sorted_x = sorted(G.degree().items(), key=operator.itemgetter(1))
    	v=list(sorted_x[0])[0]
        #case 1
    	if G.degree(v)==1 and v in set(G.nodes()).difference(set(x)):
    		G.remove_node(v)
    		if v in x:
    		     x=x.remove(v)
    		minimum_dominating(G,x,dset)
        #case2
    	elif G.degree(v)==1  and v in x:
    		w=G.neighbors(v)[0]
    		dset.append(w)
    		nw=G.neighbors(w)
    		nw.append(w)
    		G.remove_nodes_from([v,w])   		
    		x=list(set(x).difference(set(nw)))
    		minimum_dominating(G,x,dset)
        #case 3
    	elif G.degree(v)==2 and v in set(G.nodes()).difference(set(x)):
    		u1=G.neighbors(v)[0]
    		u2=G.neighbors(v)[1]
            #case 3.1
    		if u1 in dset and v not in dset:
    			dset.append(u1)
    			nu1=G.neighbors(u1)
    			nu1.append(u1)
    			G.remove_nodes_from([v,u1])
    			x=list(set(x).difference(set(nu1)))
    			minimum_dominating(G,x,dset)
            #case 3.2
    		elif v in dset and u1 not in dset and u2 not in dset:
    			dset.append(v)
    			G.remove_nodes_from([v,u1,u2])
    			x=list(set(x).difference(set([u1,u2])))
    			minimum_dominating(G,x,dset)
            #case 3.3
    		elif u1 not in dset and v not in dset:
    			G.remove_node(v)
    			minimum_dominating(G,x,dset)
        #case 4
    	elif G.degree(v)==2 and v in x:
    		u1=G.neighbors(v)[0]
    		u2=G.neighbors(v)[1]
            #case 4.1
    		if u1 in dset and v not in dset:
    			dset.append(u1)
    			nu1=G.neighbors(u1)
    			nu1.append(u1)
    			G.remove_nodes_from([v,u1])    			
    			x=list(set(x).difference(set(nu1)))
    			minimum_dominating(G,x,dset)
            #case 4.2
    		elif v in dset and u1 not in dset and u2 not in dset:
    			dset.append(v)
    			G.remove_nodes_from([v,u1,u2])
    			x=list(set(x).difference(set([u1,u2,v])))
    			minimum_dominating(G,x,dset)
            #case 4.3
    		elif u1 not in dset and v not in dset:
    			dset.append(u2)
    			nu2=G.neighbors(u2)
    			nu2.append(u2)
    			G.remove_nodes_from([v,u2])
    			x=list(set(x).difference(set(nu2)))
    			minimum_dominating(G,x,dset)
    		return dset

    		


