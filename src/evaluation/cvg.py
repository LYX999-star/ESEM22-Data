import numpy as np


def read_rsf(rsf_path):
    cluster2files = {}
    with open(rsf_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            items = line[:-1].split(' ')
            cluster_name, file_name = items[1], items[2]
            if cluster_name in cluster2files.keys():
                cluster2files[cluster_name].add(file_name)
            else:
                cluster2files[cluster_name] = set([file_name])

    clusters = []
    for key in cluster2files.keys():
        clusters.append(cluster2files[key])

    return clusters


def c2c(clusters1, clusters2):
    c2c_values = np.zeros((len(clusters1), len(clusters2)))

    for i, c1 in enumerate(clusters1):
        for j, c2 in enumerate(clusters2):
            c2c_values[i][j] = len(c1 & c2) / max(len(c1), len(c2))

    return c2c_values


def cvg(rsf1, rsf2, TH_CVG=0.67):
    clusters1, clusters2 = read_rsf(rsf1), read_rsf(rsf2)

    c2c_matrix = c2c(clusters1, clusters2)

    sim = ((c2c_matrix > TH_CVG).sum(axis=1) > 0).sum()

    return sim / len(clusters1)


if __name__ == '__main__':

    method_rsf_path = r'E:\opensource\Indirect Dependency\indirect-dependency\subspace\rsf\{}\{}.rsf'

    fout = open("A2A_Res.txt", "a")

    for project in ['caffe', 'keras', 'Theano', 'pytorch', 'tensorflow'][:]:
        method_rsf_paths = [method_rsf_path.format(method, project) for method in ['depends', 'history', 'semantic']]
        print(project, ":\t")

        len_paths = len(method_rsf_paths)
        for i in range(len_paths):
            for j in range(i + 1, len_paths):
                methoda = method_rsf_paths[i].split('\\')[-2]
                methodb = method_rsf_paths[j].split('\\')[-2]

                print('\t', methoda, methodb, cvg(method_rsf_paths[i], method_rsf_paths[j], TH_CVG=0.0))
                print('\t', methodb, methoda, cvg(method_rsf_paths[j], method_rsf_paths[i], TH_CVG=0.0))
