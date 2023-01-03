import doctest
import time

import networkx as nx

def neighbours_of_set(G, node_set):
    """
    returns a set of the neighbours of a given set of nodes
    >>> G = nx.complete_bipartite_graph(3,3)
    >>> neighbours_of_set(G, {})
    set()
    >>> neighbours_of_set(G, {1, 2})
    {3, 4, 5}

    >>> G = nx.Graph([(0, 4), (1, 5), (2, 6)])
    >>> neighbours_of_set(G, {0, 1})
    {4, 5}

    >>> G=nx.Graph([(0,3),(3,0),(0,4),(4,0),(1,4),(4,1),(2,4),(4,2)])
    >>> neighbours_of_set(G, {0, 1})
    {3, 4}

    >>> neighbours_of_set(G, {4})
    {0, 1, 2}
    """
    ret_set = {}
    for node in node_set:
        ret_set.update(G[node])

    return set(ret_set)

if __name__ == '__main__':
    t0 = time.time()
    doctest.testmod()
    t1 = time.time()
    print("Time elapsed: ", t1 - t0)