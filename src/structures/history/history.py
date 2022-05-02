import json

import networkx as nx
from src.structures.history.git2json import git2jsons, run_git_log

THRESHOLD = 0.3333
THRESHOLD_CO_CHANGED = 5


def get_history_graph(project, git_dir):
    history = get_history_with_git2json(git_dir, thr=1000, project=project)
    return history


def get_history_with_git2json(git_dir, thr=2000):
    logs = git2jsons(run_git_log(git_dir))
    logs_json = json.loads(logs)
    graph = nx.Graph()
    l = 0
    times = {}

    for commit in logs_json:
        changes = commit['changes']
        changed_files = []
        for change in changes:
            filename = change[2]
            changed_files.append(filename)
            if filename in times.keys():
                times[filename] += 1
            else:
                times[filename] = 1

        if len(changed_files) > thr:
            l += 1
            continue

        for i in range(len(changed_files)):
            for j in range(i + 1, len(changed_files)):
                if graph.has_edge(changed_files[i], changed_files[j]):
                    graph.add_edge(changed_files[i], changed_files[j],
                                   weights=1 + graph.get_edge_data(changed_files[i], changed_files[j])['weights'])
                else:
                    graph.add_edge(changed_files[i], changed_files[j], weights=1)

    history_graph = nx.DiGraph()

    for edge in graph.edges:
        a, b = edge[0], edge[1]
        weight = graph.get_edge_data(edge[0], edge[1])['weights']
        if weight >= THRESHOLD_CO_CHANGED:
            if weight / times[edge[0]] > THRESHOLD and times[a] > times[b]:
                history_graph.add_edge(a, b, weights=weight / times[edge[0]])

            if weight / times[edge[1]] > THRESHOLD and times[a] <= times[b]:
                history_graph.add_edge(b, a, weights=weight / times[edge[1]])

    return history_graph
