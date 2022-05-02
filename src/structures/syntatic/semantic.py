import hashlib
import os

import networkx
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def get_semantic_from_vector(method, project, threshold=0.66):
    vector_path = r'E:\opensource\Indirect Dependency\DL-output\words_vector\sentence_vector_output\{}_{}_vector.txt'.format(
        project, method)
    with open(vector_path, 'r', encoding='utf-8') as f:
        vectors = f.readlines()
        width = len(vectors[0].split(' '))
        height = len(vectors)
        matrix = np.zeros((height, width))
        for idx, vector in enumerate(vectors):
            matrix[idx] = [float(num) for num in vector.split(' ')]

    cos = cosine_similarity(matrix)

    cos[cos < threshold] = 0

    filenames = []
    srml_filename_path = r'E:\opensource\Indirect Dependency\DL-output\words_vector\output_dl_srcml\{}\nameFileName.txt'.format(
        project)
    project_path = r'E:\opensource\Indirect Dependency\DL-datasets\{0}'
    with open(srml_filename_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            idx = line.rindex('\\')
            preffix = line[idx + 1:-10]
            dir = project_path.format(line[:idx + 1])
            for name in os.listdir(dir):
                if preffix == name.split('.')[0]:
                    filenames.append((line[len(project) + 1:idx + 1] + name).replace('\\', '/'))
                    break;

    graph = networkx.DiGraph()

    for i in range(height):
        for j in range(height):
            if cos[i][j] > 0:
                graph.add_edge(filenames[i], filenames[j])

    return graph


def get_md5(data):
    obj = hashlib.md5("sidrsicxwersdfsaersdfsdfresdy54436jgfdsjdxff123ad".encode('utf-8'))
    obj.update(data.encode('utf-8'))
    result = obj.hexdigest()

    return result


def get_semantic_from_vector_path(vector_path, project, threshold=0.66):
    saved_path = r'E:\opensource\Indirect Dependency\indirect-dependency\evaluation\semantic_vector\{}.npy'.format(
        get_md5(vector_path)
    )

    if os.path.isfile(saved_path):
        cos = np.load(saved_path)
    else:

        with open(vector_path, 'r', encoding='utf-8') as f:
            vectors = f.readlines()
            width = len(vectors[0].split(' '))
            if vectors[0].split(' ')[-1] == '\n':
                width -= 1
            height = len(vectors)
            matrix = np.zeros((height, width))
            for idx, vector in enumerate(vectors):
                matrix[idx] = [float(num) for num in vector.split(' ') if num != '\n']

        cos = cosine_similarity(matrix)

        cos[cos < threshold] = 0

        np.save(saved_path, cos)

    filenames = []
    srml_filename_path = r'E:\opensource\Indirect Dependency\DL-output\words_vector\output_dl_srcml\{}\nameFileName.txt'.format(
        project)
    project_path = r'E:\opensource\Indirect Dependency\DL-datasets\{0}'
    with open(srml_filename_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            idx = line.rindex('\\')
            preffix = line[idx + 1:-10]
            dir = project_path.format(line[:idx + 1])
            for name in os.listdir(dir):
                if preffix == name.split('.')[0]:
                    filenames.append((line[len(project) + 1:idx + 1] + name).replace('\\', '/'))
                    break;

    graph = networkx.DiGraph()

    for pair in np.argwhere(cos > 0):
        if pair[0] != pair[1]:
            graph.add_edge(filenames[pair[0]], filenames[pair[1]])

    return graph


def get_semantic_similarity_matrix_from_vector_path(vector_path, project, threshold=0.66):
    saved_path = r'E:\opensource\Indirect Dependency\indirect-dependency\evaluation\semantic_vector\{}.npy'.format(
        get_md5(vector_path)
    )

    if os.path.isfile(saved_path):
        cos = np.load(saved_path)
    else:
        with open(vector_path, 'r', encoding='utf-8') as f:
            vectors = f.readlines()
            width = len(vectors[0].split(' '))
            if vectors[0].split(' ')[-1] == '\n':
                width -= 1
            height = len(vectors)
            matrix = np.zeros((height, width))
            for idx, vector in enumerate(vectors):
                matrix[idx] = [float(num) for num in vector.split(' ') if num != '\n']

        cos = cosine_similarity(matrix)

        cos[cos < threshold] = 0

        np.save(saved_path, cos)

    return cos


def get_tf_idf_graph(project):
    tf_idf_path = r'E:\opensource\Indirect Dependency\DL-output\words_vector\tfidf_vec\{}_vec.txt'.format(project)
    return get_semantic_from_vector_path(tf_idf_path, project)


def get_tf_idf_similarity_matrix(project):
    tf_idf_path = r'E:\opensource\Indirect Dependency\DL-output\words_vector\tfidf_vec\{}_vec.txt'.format(project)
    return get_semantic_similarity_matrix_from_vector_path(tf_idf_path, project)


def combine_similarity_matrixs(similarity_matrixs, project):
    combined_matrix = (similarity_matrixs[0] > 0)
    for matrix in similarity_matrixs[1:]:
        combined_matrix = combined_matrix & (matrix > 0)

    filenames = []
    srml_filename_path = r'E:\opensource\Indirect Dependency\DL-output\words_vector\output_dl_srcml\{}\nameFileName.txt'.format(
        project)
    project_path = r'E:\opensource\Indirect Dependency\DL-datasets\{0}'
    with open(srml_filename_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            idx = line.rindex('\\')
            preffix = line[idx + 1:-10]
            dir = project_path.format(line[:idx + 1])
            for name in os.listdir(dir):
                if preffix == name.split('.')[0]:
                    filenames.append((line[len(project) + 1:idx + 1] + name).replace('\\', '/'))
                    break;

    semantic_graph = networkx.DiGraph()

    for pair in np.argwhere(combined_matrix):
        if pair[0] != pair[1]:
            semantic_graph.add_edge(filenames[pair[0]], filenames[pair[1]])

    return semantic_graph


def get_semantic_graph_from_similarity_matrix(project):
    methods = ['doc2vec', 'sentenceBert']
    similarity_matrixs = []
    for method in methods:
        word_vector_path = r'E:\opensource\Indirect Dependency\DL-output\words_vector\sentence_vector_output\{}_{}_vector.txt'.format(
            project, method)
        matrix = get_semantic_similarity_matrix_from_vector_path(word_vector_path, project, threshold=0.66)
        similarity_matrixs.append(matrix)

    similarity_matrixs.append(get_tf_idf_similarity_matrix(project))

    semantic_graph = combine_similarity_matrixs(similarity_matrixs, project)

    return semantic_graph

