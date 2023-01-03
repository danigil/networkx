import cython_improved
import standard
import time

import networkx as nx

cython_envy_free_matching = cython_improved.envy_free_matching
standard_envy_free_matching = standard.envy_free_matching

cython_minimum_weight_envy_free_matching = cython_improved.minimum_weight_envy_free_matching
standard_minimum_weight_envy_free_matching = standard.minimum_weight_envy_free_matching


def generate_marriable_bipartite_graph(size: int):
    """
    generate_marriable_bipartite_graph

    input: positive number
    output: bipartite graph with both sets of cardinality = size each node has one edge to exactly one node.

    >>> generate_marriable_bipartite_graph(3).edges
    [(0, 3), (1, 4), (2, 5)]
    """
    return nx.Graph([(i, i + size) for i in range(size)])


def generate_odd_path(size: int):
    """
    generate_odd_path

    input: positive odd(!!) number
    output: bipartite graph with one set of cardinality = size and one set of cardinality = size - 1
    with the shape of an odd path.

    >>> generate_odd_path(3).edges
    [(0, 3), (1, 3), (1, 4), (2, 4), (3, 0), (3, 1), (4, 1), (4, 2)]

    """
    if size % 2 == 0: raise Exception

    edges = [(0, size)]

    actions = {
        0: lambda: edges.append((edges[-1][0], edges[-1][1] + 1)),

        1: lambda: edges.append((edges[-1][0] + 1, edges[-1][1]))
    }

    for i in range(1, size + 1):
        actions[i % 2]()
    return nx.Graph(edges)


def run_cython(func_name, *args, **kwargs):
    if func_name == envy_free_matching_name:
        func = cython_envy_free_matching
    else:
        func = cython_minimum_weight_envy_free_matching

    func(*args, **kwargs)


def run_standard(func_name, *args, **kwargs):
    if func_name == envy_free_matching_name:
        func = standard_envy_free_matching
    else:
        func = standard_minimum_weight_envy_free_matching

    func(*args, **kwargs)


envy_free_matching_name = 'envy_free_matching'
minimum_weight_envy_free_matching_name = 'minimum_weight_envy_free_matching'

def time_func(func, *args, **kwargs):
    t0 = time.time()
    func(*args, **kwargs)
    return time.time() - t0

if __name__ == '__main__':
    sizes = [10, 100, 10000]
    for size in sizes:
        G = nx.bipartite.random_graph(size, size,0.1)
        print('--------------------------')
        print(f'running envy_free_matching with G={G}')
        cython_time = time_func(run_cython, envy_free_matching_name, G)
        standard_time = time_func(run_standard, envy_free_matching_name, G)
        print(f'cython: {cython_time}, standard: {standard_time}, ratio(standard_time/cython_time): {standard_time/cython_time}')
        print('--------------------------')

