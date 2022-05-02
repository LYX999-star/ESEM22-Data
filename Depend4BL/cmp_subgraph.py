from queue import Queue


# Calculate corresponding subgraph based on the incoming dependency graph
def cmp_subgraph(G):
    subgraphs = []

    for first_node in G.nodes():
        subgraph = []
        q = Queue()
        q.put(first_node)
        used_nodes = set()
        used_nodes.add(first_node)
        while not q.empty():
            node = q.get()
            subgraph.append(node)
            for sub_node in G[node]:
                if not sub_node in used_nodes:
                    used_nodes.add(sub_node)
                    q.put(sub_node)

        subgraphs.append(subgraph)

    return subgraphs
