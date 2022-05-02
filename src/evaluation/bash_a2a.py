import igraph
import sys
import os


def a2a(file_A, file_B):
    f = open(file_A, "r")
    lines = f.readlines()
    f.close()

    a1 = {}
    for line in lines:
        templist = line.strip().split(" ")
        if templist[1] not in a1:
            a1[templist[1]] = []
            pass
        a1[templist[1]].append(templist[2])

    f = open(file_B, "r")
    lines = f.readlines()
    f.close()

    a2 = {}
    for line in lines:
        templist = line.strip().split(" ")
        if templist[1] not in a2:
            a2[templist[1]] = []
            pass
        a2[templist[1]].append(templist[2])

    match_type = []
    for i in range(0, len(a1)):
        match_type.append(0)
        pass

    for i in range(0, len(a2)):
        match_type.append(1)
        pass

    edge_dict = {}

    for temp1 in range(0, len(a1)):
        for temp2 in range(0, len(a2)):
            edge_dict[(temp1, temp2 + len(a1))] = len(set(list(a1.values())[temp1]) & set(list(a2.values())[temp2]))
            pass

    g = igraph.Graph()
    g.add_vertices(len(a1) + len(a2))

    g.add_edges(edge_dict.keys())

    matching = g.maximum_bipartite_matching(types=match_type, weights=list(edge_dict.values()))

    removeA = []
    moveAB = []
    addB = []

    for i in range(0, len(a1) + len(a2)):
        if i < len(a1):
            if matching.match_of(i) == None:
                removeA.append(i)
                pass
            else:
                moveAB.append((i, matching.match_of(i)))
                pass
            pass
        else:
            if matching.match_of(i) == None:
                addB.append(i)
            pass
        pass

    mto = 0

    for i in removeA:
        mto += len(list(a1.values())[i])
        mto += 1
        pass
    for i in addB:
        mto += len(list(a2.values())[i - len(a1)])
        mto += 1
        pass
    for temp in moveAB:
        mto += len(list(a1.values())[temp[0]]) - edge_dict[temp] + len(list(a2.values())[temp[1] - len(a1)]) - \
               edge_dict[temp]
        pass

    aco1 = sum(map(len, a1.values())) + len(a1)
    aco2 = sum(map(len, a2.values())) + len(a2)

    a2a = 1 - float(mto) / (float(aco1) + float(aco2))
    return a2a


if __name__ == "__main__":
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

                print('\t', methoda, methodb, a2a(method_rsf_paths[i], method_rsf_paths[j]))
