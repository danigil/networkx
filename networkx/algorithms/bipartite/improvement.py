import networkx.algorithms.bipartite.envy_free_matching as nx
import networkx as net
import matplotlib.pyplot as plt
import cython
import time


def improved_EFM(G, M=None, top_nodes=None):
    # M=cython.cfunc(net.algorithms.bipartite.maximum_matching(G))
    cython.cfunc(nx._EFM_partition(G, M, top_nodes))


def improved_Envy_free_matching(G, top_nodes=None):
    cython.cfunc(nx.envy_free_matching(G, top_nodes))


def improved_Envy_free_weighted_graph(G, top_nodes=None):
    cython.cfunc(nx.minimum_weight_envy_free_matching(G, top_nodes))


def compare_envy_free_matching():
    sizes1 = []
    times1 = []
    sizes2 = []
    times2 = []
    for i in range(100, 150):
        Graph = net.complete_bipartite_graph(i, i)
        t1 = time.time()
        nx.envy_free_matching(Graph)
        t2 = time.time()
        times1.append(t2 - t1)
        sizes1.append(i)
        t1 = time.time()
        improved_Envy_free_matching(Graph)
        t2 = time.time()
        times2.append(t2 - t1)
        sizes2.append(i)

    fig, (ax1, ax2) = plt.subplots(1, 2, constrained_layout=True, sharey=True)
    ax1.plot(sizes1, times1)
    ax1.set_title('Original envy-free matching (Python)', fontsize=9)
    ax1.set_xlabel('graph size')
    ax1.set_ylabel('time')

    ax2.plot(sizes2, times2)
    ax2.set_title('Improved envy-free matching (Cython)', fontsize=9)
    ax2.set_xlabel('graph size')
    ax2.set_ylabel('time')

    fig.suptitle('Envy free matching Python vs Cython', fontsize=11)
    plt.show()


def compare_EFM_PARTITION():
    sizes1 = []
    times1 = []
    sizes2 = []
    times2 = []
    for i in range(150, 170):
        Graph = net.complete_bipartite_graph(i, i)
        t1 = time.time()
        nx._EFM_partition(Graph)
        t2 = time.time()
        times1.append(t2 - t1)
        sizes1.append(i)
        t1 = time.time()
        improved_EFM(Graph)
        t2 = time.time()
        times2.append(t2 - t1)
        sizes2.append(i)

    fig, (ax1, ax2) = plt.subplots(1, 2, constrained_layout=True, sharey=True)
    ax1.plot(sizes1, times1)
    ax1.set_title('Original EFM partition (Python)', fontsize=9)
    ax1.set_xlabel('graph size')
    ax1.set_ylabel('time')

    ax2.plot(sizes2, times2)
    ax2.set_title('Improved EFM partition (Cython)', fontsize=9)
    ax2.set_xlabel('graph size')
    ax2.set_ylabel('time')

    fig.suptitle('EFM partition Python vs Cython', fontsize=11)
    plt.show()


def compare_minimum_weight_EFM():
    sizes1 = []
    times1 = []
    sizes2 = []
    times2 = []
    for i in range(150, 170):
        Graph = net.complete_bipartite_graph(i, i)
        t1 = time.time()
        nx.minimum_weight_envy_free_matching(Graph)
        t2 = time.time()
        times1.append(t2 - t1)
        sizes1.append(i)
        t1 = time.time()
        improved_Envy_free_weighted_graph(Graph)
        t2 = time.time()
        times2.append(t2 - t1)
        sizes2.append(i)

    fig, (ax1, ax2) = plt.subplots(1, 2, constrained_layout=True, sharey=True)
    ax1.plot(sizes1, times1)
    ax1.set_title('Original minimum-weight EFM (Python)', fontsize=9)
    ax1.set_xlabel('graph size')
    ax1.set_ylabel('time')

    ax2.plot(sizes2, times2)
    ax2.set_title('Improved minimum-weight EFM (Cython)', fontsize=9)
    ax2.set_xlabel('graph size')
    ax2.set_ylabel('time')

    fig.suptitle('Minimum-weight maximum cardinality EFM Python vs Cython', fontsize=11)
    plt.show()




if __name__ == '__main__':
    print(f"Comparing the envy free matching improvement")
    compare_envy_free_matching()
    time.sleep(5)
    print(f"Comparing EFM partition")
    compare_EFM_PARTITION()
    time.sleep(5)
    print(f"Comparing minimum weight maximum cardinality envy free matching")
    compare_minimum_weight_EFM()

