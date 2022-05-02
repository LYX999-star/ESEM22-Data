import csv
import json
import os


def save_dependency_to_json(G, dependency_type, project):
    saved_dir = r'E:\opensource\Indirect Dependency\indirect-dependency\subspace\structures\{}'.format(dependency_type)
    os.makedirs(saved_dir, exist_ok=True)
    saved_path = r'E:\opensource\Indirect Dependency\indirect-dependency\subspace\structures\{}\{}.json'.format(
        dependency_type, project)

    res = {}

    node2num = {}
    nodes = []

    for idx, node in enumerate(G.nodes):
        node2num[node] = idx
        nodes.append(node)

    res['variables'] = nodes
    edges = []
    for edge in G.edges:
        tmp = {}
        tmp['src'] = node2num[edge[0]]
        tmp['dest'] = node2num[edge[1]]
        edges.append(tmp)
    res['cells'] = edges

    s = json.dumps(res)

    with open(saved_path, 'w', encoding='utf-8') as f:
        f.write(s)
