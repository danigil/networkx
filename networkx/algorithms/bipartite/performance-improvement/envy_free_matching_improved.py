import doctest
import time

import networkx as nx
import cppyy
cpp_set = cppyy.gbl.std.set
# cppyy.include('<iostream>')
# cppyy.include('<set>')

# def neighbours_of_set(G, node_set):
#     """
#     returns a set of the neighbours of a given set of nodes
#     >>> G = nx.complete_bipartite_graph(3,3)
#     >>> __neighbours_of_set__(G, {})
#     set()
#     >>> __neighbours_of_set__(G, {1, 2})
#     {3, 4, 5}
#
#     >>> G = nx.Graph([(0, 4), (1, 5), (2, 6)])
#     >>> __neighbours_of_set__(G, {0, 1})
#     {4, 5}
#
#     >>> G=nx.Graph([(0,3),(3,0),(0,4),(4,0),(1,4),(4,1),(2,4),(4,2)])
#     >>> __neighbours_of_set__(G, {0, 1})
#     {3, 4}
#
#     >>> __neighbours_of_set__(G, {4})
#     {0, 1, 2}
#     """
#     ret_set = {}
#     for node in node_set:
#         ret_set.update(G[node])
#
#     return set(ret_set)

# cppyy.cppdef("""
# #include <iostream>
# #include <set>
#
# void example()
# {
#   std::set<char> a;
#   a.insert('G');
#   a.insert('F');
#   a.insert('G');
#   for(auto& str: a)
#   {
#     std::cout << str << " ";
#   }
#   std::cout << "\n";
# }
# """)
#
# cppyy.gbl.example()
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
    cpp_node_set = cpp_set[int](list(node_set))

    ret_set = cpp_set[int]()
    for node in cpp_node_set:
        ret_set.insert(list(G[node]))

    return set(ret_set)

if __name__ == '__main__':
    t0 = time.clock()
    doctest.testmod()
    t1 = time.clock() - t0
    print("Time elapsed: ", t1 - t0)