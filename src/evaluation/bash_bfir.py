import os


def subspaces_to_rsf(arch_root_subspace, project, dependency_type):
    rsf_path = r'E:\opensource\Indirect Dependency\indirect-dependency\subspace\rsf\{}\\'.format(dependency_type)
    os.makedirs(rsf_path, exist_ok=True)

    with open(rsf_path + '{}.rsf'.format(project), 'w', encoding='utf-8') as out:
        for idx, subspace in enumerate(arch_root_subspace):
            cluster_name = 'cluster-' + str(idx)
            for file in subspace:
                line = 'contain {0} {1}\n'.format(cluster_name, file.replace(' ', ''))
                # print(line)
                out.write(line)


def get_result_set(arch_root_subspace, target_set):
    result_set = set()
    for subspace in arch_root_subspace:
        for file in subspace:
            if file in target_set:
                result_set.add(file)
    return result_set


def cmp_bcir(result_set, target_set, file2churn):
    churn_result_set = 0
    churn_bl = 0
    for file in target_set:
        if file in result_set:
            churn_result_set += file2churn[file]
        else:
            churn_bl += file2churn[file]

    if churn_result_set == 0:
        return 0
    else:
        return (churn_result_set / len(result_set)) * ((len(target_set) - len(result_set)) / churn_bl) - 1


def cmp_bcfr(result_set, target_set, file2fre):
    fre_result_set = 0
    fre_bl = 0
    for file in target_set:
        if file in result_set:
            fre_result_set += file2fre[file]
        else:
            fre_bl += file2fre[file]

    if fre_result_set == 0:
        return 0
    else:
        return (fre_result_set / len(result_set)) * ((len(target_set) - len(result_set)) / fre_bl) - 1
