import csv
import operator
import os
import random

import numpy as np

from Depend4BL.bug_fixed_file import get_bug_fixed_files
from Depend4BL.read_structure import read_structure
from subspace import cmp_subspace


# Interplay Calculation:贪心覆盖
def compute_interactions(target_set, HS):
    # 能够覆盖target_set的subspace的集合
    used = np.zeros(len(HS))
    arch_root_subspace = []
    covered_target_file_num = 0
    len_target_set = len(target_set)
    covered_subspace_file_num = 0

    while len(target_set) > 0:
        # 记录最大的覆盖
        max_subspace = []
        max_cover = []
        max_count = 0
        max_idx = -1

        # 遍历HS中的全部子层次结构,并计数
        for idx, subspace in enumerate(HS):
            # subspace = subspace.split('###')
            if used[idx] == 1:
                continue
            tmp_cover = []
            tmp_count = 0
            for file in subspace:
                if file in target_set:
                    tmp_cover.append(file)
                    tmp_count += 1
            # 用最小的集合去覆盖最大的target文件数
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
        # 无法继续覆盖
        if max_count == 0:
            break;

        # 使用max_cover覆盖target_set
        for covered_file in max_cover:
            target_set.remove(covered_file)

        # 删除max_subspace
        # HS.remove('###'.join(max_subspace))
        used[max_idx] = 1
        covered_subspace_file_num += len(max_subspace)

        # 记录subspace并计数
        arch_root_subspace.append(max_subspace)
        covered_target_file_num += max_count
    # 计算查准率，查全率
    # 查准率
    if covered_target_file_num == 0:
        precision = 0.0
    else:
        precision = covered_target_file_num / covered_subspace_file_num
    # 查全率
    recall = covered_target_file_num / len_target_set
    # f1
    if precision + recall == 0:
        f1 = 0
    else:
        f1 = 2 * (precision * recall) / (precision + recall)

    return precision, recall, f1, arch_root_subspace


if __name__ == '__main__':

    '''
    计算三种依赖的组合在bug修复上的效果：precision, recall, f1
    '''
    projects = ['caffe', 'keras', 'Theano', 'pytorch', 'tensorflow']

    '''
        example:计算caffe项目的
    '''

    bug_fixed_path = r'E:\opensource\Indirect Dependency\ESEM22-Data\Bug Fix Collection\bug_fixed_files\caffe.txt'
    # 读取bug_fixed_files
    bug_fixed_files = get_bug_fixed_files(bug_fixed_path)
    # 读取dependency structure
    structure_path = r'E:\opensource\Indirect Dependency\ESEM22-Data\Dependency Structures\semantic\caffe.json'
    structure = read_structure(structure_path)

    # 根据依赖图计算其子层次结构:依赖图中的节点名称为根路径开头的文件名
    subspaces = cmp_subspace(structure)
    precision, recall, f1, arch_root_subspace = compute_interactions(set(bug_fixed_files), subspaces)

    print(precision, recall, f1)
