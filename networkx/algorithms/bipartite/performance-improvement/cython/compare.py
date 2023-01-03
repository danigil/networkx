from cython_improved import neighbours_of_set
import time

import networkx as nx

if __name__ == '__main__':
    t0 = time.time()

    G = nx.complete_bipartite_graph(3, 3)
    neighbours_of_set(G, {})

    neighbours_of_set(G, {1, 2})

    G = nx.Graph([(0, 4), (1, 5), (2, 6)])
    neighbours_of_set(G, {0, 1})

    G = nx.Graph([(0, 3), (3, 0), (0, 4), (4, 0), (1, 4), (4, 1), (2, 4), (4, 2)])
    neighbours_of_set(G, {0, 1})

    neighbours_of_set(G, {4})

    t1 = time.time()

    print("Time elapsed: ", t1 - t0)