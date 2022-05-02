import argparse
import csv
import operator
import os
import random

import numpy as np

from read_bug_fixed_files import get_bug_fixed_files
from read_structure import read_structure
from cmp_subgraph import cmp_subgraph


# Interplay Calculation: Computing interactions between dependency structures and bug fixed files using greedy strategies
def compute_interactions(target_set, HS):
    used = np.zeros(len(HS))
    arch_root_subspace = []
    covered_target_file_num = 0
    len_target_set = len(target_set)
    covered_subspace_file_num = 0

    while len(target_set) > 0:
        max_subspace = []
        max_cover = []
        max_count = 0
        max_idx = -1

        for idx, subspace in enumerate(HS):
            if used[idx] == 1:
                continue
            tmp_cover = []
            tmp_count = 0
            for file in subspace:
                if file in target_set:
                    tmp_cover.append(file)
                    tmp_count += 1
            if tmp_count > max_count:
                max_count = tmp_count
                max_cover = tmp_cover
                max_subspace = subspace
                max_idx = idx
            elif tmp_count == max_count and len(max_subspace) > len(subspace):
                max_count = tmp_count
                max_cover = tmp_cover
                max_subspace = subspace
                max_idx = idx

        if max_count == 0:
            break;

        for covered_file in max_cover:
            target_set.remove(covered_file)

        used[max_idx] = 1
        covered_subspace_file_num += len(max_subspace)

        arch_root_subspace.append(max_subspace)
        covered_target_file_num += max_count

    if covered_target_file_num == 0:
        precision = 0.0
    else:
        precision = covered_target_file_num / covered_subspace_file_num

    recall = covered_target_file_num / len_target_set
    if precision + recall == 0:
        f1 = 0
    else:
        f1 = 2 * (precision * recall) / (precision + recall)

    return precision, recall, f1, arch_root_subspace


def main():
    parser = argparse.ArgumentParser(description="""Calculating the interaction between dependency structures and bug fix files
                                                     For example: python depend4bl.py --bug-fixed "caffe.txt" --structure"caffe.json"
                                                     
                                                     """)
    parser.add_argument('--bug-fixed', type=str,
                        help="Path to the file containing the collection of bug fixes")
    parser.add_argument('--structure', type=str,
                        help="The name of the Jira repository of the project.")

    args = parser.parse_args()

    bug_fixed_path = args.bug_fixed
    structure_path = args.structure

    bug_fixed_files = get_bug_fixed_files(bug_fixed_path)

    structure = read_structure(structure_path)

    subspaces = cmp_subgraph(structure)
    precision, recall, f1, arch_root_subspace = compute_interactions(set(bug_fixed_files), subspaces)

    print('===============================')
    print('Precision:', '%.2f%%'%(precision*100))
    print('Recall:', '%.2f%%'%(recall*100))
    print('F1-Measure:', '%.2f%%'%(f1*100))
    print('===============================')



if __name__ == '__main__':
    main()

    '''
        example:Calculating the interaction of historical dependencies with bug fixed files on caffe projects
            '''
    # bug_fixed_path = r'E:\opensource\Indirect Dependency\ESEM22-Data\Bug Fix Collection\bug_fixed_files\caffe.txt'
    # # 读取bug_fixed_files
    # bug_fixed_files = get_bug_fixed_files(bug_fixed_path)
    # # 读取dependency structure
    # structure_path = r'E:\opensource\Indirect Dependency\ESEM22-Data\Dependency Structures\semantic\caffe.json'
    # structure = read_structure(structure_path)
    # # 根据依赖图计算其子层次结构:依赖图中的节点名称为根路径开头的文件名
    # subspaces = cmp_subgraph(structure)
    # precision, recall, f1, arch_root_subspace = compute_interactions(set(bug_fixed_files), subspaces)
    # print('===============================')
    # print('Precision:', '%.2f%%'%(precision*100))
    # print('Recall:', '%.2f%%'%(recall*100))
    # print('F1-Measure:', '%.2f%%'%(f1*100))
    # print('===============================')

