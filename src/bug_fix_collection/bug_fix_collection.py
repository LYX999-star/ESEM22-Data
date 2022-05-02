import csv
import operator
import os
from git2json import *


def find_bug_fixed_files(git_dir, bug_fixed_path, idx=7, header=True, project=''):
    logs = git2jsons(run_git_log(git_dir))
    logs_json = json.loads(logs)

    commits = get_bug_fixed_files(bug_fixed_path, idx=idx, header=True)

    def get_commit_files(logs):
        commit_files = {}

        for log in logs:
            commit_files[log['commit']] = log['changes']

        return commit_files

    commit2changed_files = get_commit_files(logs_json)

    bug_fixed_files = set()
    suffix = set(['cpp', 'hpp', 'c', 'h', 'py'])
    not_match = 0
    for commit_id in commits:
        if commit_id not in commit2changed_files.keys():
            not_match += 1
            continue
        for changed_file in commit2changed_files[commit_id]:
            filename = changed_file[2]
            if filename.split('.')[-1] in suffix:
                bug_fixed_files.add(filename)

    os.makedirs('bug_fixed_files', exist_ok=True)
    with open('bug_fixed_files/{}.txt'.format(project), 'w', encoding='utf-8') as f:
        f.write('\n'.join(bug_fixed_files))

    return bug_fixed_files


def find_bug_fixed_files_ranked(git_dir, bug_fixed_path, idx=7, header=True, project=''):
    if os.path.isfile('git2json/{}.txt'.format(project)):
        with open('git2json/{}.txt'.format(project), encoding='utf-8') as f:
            s = f.read()
            logs = s
    else:
        logs = git2jsons(run_git_log(git_dir))
        os.makedirs('git2json', exist_ok=True)
        with open('git2json/{}.txt'.format(project), 'w', encoding='utf-8') as f:
            f.write(logs)

    logs_json = json.loads(logs)

    commits = get_bug_fixed_files(bug_fixed_path, idx=idx, header=True)

    def get_commit_files(logs):
        commit_files = {}
        for log in logs:
            commit_files[log['commit']] = log['changes']

        return commit_files

    commit2changed_files = get_commit_files(logs_json)

    bug_fixed_files = set()
    bug_fixed_files_fre = {}
    bug_fixed_files_churn = {}
    suffix = set(['cpp', 'hpp', 'c', 'h', 'py'])
    not_match = 0
    for commit_id in commits:
        if commit_id not in commit2changed_files.keys():
            not_match += 1
            continue
        for changed_file in commit2changed_files[commit_id]:
            filename = changed_file[2]
            if filename.split('.')[-1] in suffix:
                bug_fixed_files.add(filename)

                if filename in bug_fixed_files_churn.keys():
                    try:
                        bug_fixed_files_churn[filename] += (int)(changed_file[0] + changed_file[1])
                    except:
                        bug_fixed_files_churn[filename] += 0
                    bug_fixed_files_fre[filename] += 1
                else:
                    try:
                        bug_fixed_files_churn[filename] = (int)(changed_file[0] + changed_file[1])
                    except:
                        bug_fixed_files_churn[filename] = 0
                    bug_fixed_files_fre[filename] = 1

    return ranked_by_files_dict(bug_fixed_files_churn), ranked_by_files_dict(bug_fixed_files_fre)


def ranked_by_files_dict(files_dict):
    sorted_files_dict = sorted(files_dict.items(), key=operator.itemgetter(1), reverse=True)
    ranked_files = []
    for i in range(1, 11):
        ranked_x = []
        for k in sorted_files_dict[:int(len(sorted_files_dict) * 0.1 * i)]:
            ranked_x.append(k[0])

        ranked_files.append(ranked_x)

    return ranked_files


def get_bug_fixed_files(bug_fixed_path, idx=7, header=True):
    with open(bug_fixed_path, encoding='utf-8') as f:
        reader = csv.reader(f)
        commits = []

        for row in reader:
            if header:
                header = False
                continue
            commit = row[idx].split('/commit/')[-1]
            commits.append(commit)
    return commits
