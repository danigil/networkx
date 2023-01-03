from cython_improved import envy_free_matching
import time

import networkx as nx

if __name__ == '__main__':
    t0 = time.time()

    Graph = nx.complete_bipartite_graph(3, 3)
    envy_free_matching(Graph)

    Graph = nx.Graph([(0, 3), (3, 0), (0, 4), (4, 0), (1, 4), (4, 1), (2, 4), (4, 2)])
    envy_free_matching(Graph)

    Graph = nx.Graph([(0, 3), (3, 0), (1, 3), (3, 1), (1, 4), (4, 1), (2, 4), (4, 2)])
    envy_free_matching(Graph)

    Graph = nx.Graph(
        [(0, 6), (6, 0), (1, 6), (6, 1), (1, 7), (7, 1), (2, 6), (6, 2), (2, 8), (8, 2), (3, 9), (9, 3), (3, 6), (6, 3),
         (4, 8), (8, 4), (4, 7), (7, 4), (5, 9), (9, 5)])
    envy_free_matching(Graph)

    t1 = time.time()

    print("Time elapsed: ", t1 - t0)