import json
import os

import networkx as nx

from src.structures.history.history import get_history_with_git2json
from src.structures.syntatic.semantic import get_semantic_graph_from_similarity_matrix


def combine_and(project, name, *graphs):
    saved_path = r'E:\opensource\Indirect Dependency\indirect-dependency\subspace\graphs\{}\{}.txt'.format(project,
                                                                                                           name)
    if os.path.isfile(saved_path):
        combined_graph = load_graph(saved_path)
    else:
        combined_graph = nx.DiGraph()
        edges = {}
        for graph in graphs:
            for edge in graph.edges:
                key = edge[0] + ' ' + edge[1]
                if key in edges:
                    edges[key] += 1
                else:
                    edges[key] = 1
        len_graphs = len(graphs)
        for edge in edges.keys():
            if edges[edge] == len_graphs:
                edge = edge.split(' ')
                combined_graph.add_edge(edge[0], edge[1])
        save_graph(combined_graph, saved_path)
    return combined_graph


def combine_or(project, name, *graphs):
    saved_path = r'E:\opensource\Indirect Dependency\indirect-dependency\subspace\graphs\{}\{}.txt'.format(project,
                                                                                                           name)
    if os.path.isfile(saved_path):
        combined_graph = load_graph(saved_path)
    else:
        combined_graph = nx.DiGraph()
        for graph in graphs:
            for edge in graph.edges:
                combined_graph.add_edge(edge[0], edge[1])
        save_graph(combined_graph, saved_path)
    return combined_graph


def get_combinations(project):
    syntactic, history, semantic = get_all_dependency(project)

    # syntactic_and_history
    syntactic_and_history = combine_and(project, 'syntactic_and_history', syntactic, history)
    # syntactic_and_semantic
    syntactic_and_semantic = combine_and(project, 'syntactic_and_semantic', syntactic, semantic)
    # history_and_semantic
    history_and_semantic = combine_and(project, 'history_and_semantic', history, semantic)
    # syntactic_and_history_and_semantic
    syntactic_and_history_and_semantic = combine_and(project, 'syntactic_and_history_and_semantic', syntactic, history,
                                                     semantic)

    # syntactic_or_history
    syntactic_or_history = combine_or(project, 'syntactic_or_history', syntactic, history)
    # syntactic_or_semantic
    syntactic_or_semantic = combine_or(project, 'syntactic_or_semantic', syntactic, semantic)
    # history_or_semantic
    history_or_semantic = combine_or(project, 'history_or_semantic', history, semantic)
    # syntactic_or_history_or_semantic
    syntactic_or_history_or_semantic = combine_or(project, 'syntactic_or_history_or_semantic', syntactic, history,
                                                  semantic)

    graphs = {}
    graphs['syntactic_and_history'] = syntactic_and_history
    graphs['syntactic_and_semantic'] = syntactic_and_semantic
    graphs['history_and_semantic'] = history_and_semantic
    graphs['syntactic_and_history_and_semantic'] = syntactic_and_history_and_semantic
    graphs['syntactic_or_history'] = syntactic_or_history
    graphs['syntactic_or_semantic'] = syntactic_or_semantic
    graphs['history_or_semantic'] = history_or_semantic
    graphs['syntactic_or_history_or_semantic'] = syntactic_or_history_or_semantic

    return graphs


def get_combinations_all_or(project):
    syntactic, history, semantic = get_all_dependency(project)

    syntactic_or_history_or_semantic = combine_or(project, 'syntactic_or_history_or_semantic', syntactic, history,
                                                  semantic)

    return syntactic_or_history_or_semantic


def get_all_dependency(project):
    saved_format = r'E:\opensource\Indirect Dependency\indirect-dependency\subspace\graphs\{}\{}.txt'
    git_dir = 'E:\\opensource\\Indirect Dependency\\DL-datasets\\{0}\\.git'.format(project)
    prefix = 'E:\\opensource\\Indirect Dependency\\DL-datasets\\{0}\\'.format(project)
    depends_dir_py = 'E:\\opensource\\Indirect Dependency\\DL-output\\depends\\{0}_py.json'.format(project)
    depends_dir_cpp = 'E:\\opensource\\Indirect Dependency\\DL-output\\depends\\{0}_cpp.json'.format(project)

    # syntactic
    dependency_type = 'syntactic'
    saved_path = saved_format.format(project, dependency_type)
    if os.path.isfile(saved_path):
        syntactic_graph = load_graph(saved_path)
    else:
        syntactic_graph = get_depends(project, depends_dir_py, depends_dir_cpp, len(prefix))
        save_graph(syntactic_graph, saved_path)

    # history
    dependency_type = 'history'
    saved_path = saved_format.format(project, dependency_type)
    if os.path.isfile(saved_path):
        history_graph = load_graph(saved_path)
    else:
        history_graph = get_history_with_git2json(project, git_dir)
        save_graph(history_graph, saved_path)

    # semantic
    dependency_type = 'semantic'
    saved_path = saved_format.format(project, dependency_type)
    if os.path.isfile(saved_path):
        semantic_graph = load_graph(saved_path)
    else:
        semantic_graph = get_semantic_graph_from_similarity_matrix(project)
        save_graph(semantic_graph, saved_path)

    return syntactic_graph, history_graph, semantic_graph


def get_depends(project, depends_dir_py, depends_dir_cpp, prefix, types=set([])):
    depends_graph = nx.DiGraph()
    used_thresh = len(types) > 0
    for depends_dir in [depends_dir_py, depends_dir_cpp]:
        with open(depends_dir) as f:
            s = f.read()
            depends_json = json.loads(s)
            variables = depends_json['variables']
            num2file = {}
            for i in range(0, len(variables)):
                filename = variables[i][prefix:]
                num2file[i] = filename.replace('\\', '/')

            cells = depends_json['cells']

            for cell in cells:

                node0, node1 = num2file[cell['src']], num2file[cell['dest']]

                if used_thresh:
                    values = cell['values']
                    for value in values:
                        print(value)
                        if value in types:
                            depends_graph.add_edge(node0, node1)
                            break
                else:
                    depends_graph.add_edge(node0, node1)

    return depends_graph


def save_graph(graph, path):
    os.makedirs(path[:path.rindex('\\')], exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        for edge in graph.edges:
            f.write('{} {}\n'.format(edge[0], edge[1]))


def load_graph(path):
    graph = nx.DiGraph()
    with open(path, encoding='utf-=8') as f:
        lines = f.readlines()
        for line in lines:
            edge = line[:-1].split(' ')
            graph.add_edge(edge[0], edge[1])
    return graph
