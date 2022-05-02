import json

import networkx as nx


# 从xxx.json文件中读取依赖结构，返回networkx有向图
def read_structure(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        structure = json.loads(s)
        variables = structure['variables']
        cells = structure['cells']
    idx2node = {}
    for idx, node in enumerate(variables):
        idx2node[idx] = node

    G = nx.DiGraph()

    for cell in cells:
        G.add_edge(idx2node[cell['src']], idx2node[cell['dest']])

    return G
