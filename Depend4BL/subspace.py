from queue import Queue


# 根据传入的依赖图，计算其对应的子空间
def cmp_subspace(G):
    # 子层次结构集合
    subspaces = []

    for first_node in G.nodes():
        # 子层次结构
        subspace = []
        # 先进先出队列
        q = Queue()
        q.put(first_node)
        used_nodes = set()
        used_nodes.add(first_node)
        while not q.empty():
            node = q.get()
            subspace.append(node)
            for sub_node in G[node]:
                if not sub_node in used_nodes:
                    used_nodes.add(sub_node)
                    q.put(sub_node)

        subspaces.append(subspace)

    return subspaces
