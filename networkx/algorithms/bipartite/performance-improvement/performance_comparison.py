import cppyy_improved
import time

import networkx as nx

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import envy_free_matching

if __name__ == '__main__':

    G = nx.complete_bipartite_graph(3,3)

    start_1 = time.time_ns()
    result_1 = envy_free_matching.neighbours_of_set(G, {1})
    end_1 = time.time_ns()

    time_1 = end_1-start_1
    print(f'without improvement: {time_1}, result: {result_1}')

    start_2 = time.time_ns()
    result_2 = envy_free_matching_improved.neighbours_of_set(G, {1})
    end_2 = time.time_ns()

    time_2 = end_2 - start_2
    print(f'with improvement: {time_2}, result: {result_2}')

    print(f'improvement is faster: {time_2 < time_1}, ratio: {time_1/time_2}')

