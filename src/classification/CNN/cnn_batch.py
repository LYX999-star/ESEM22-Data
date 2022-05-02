# coding:utf-8
import csv
import time
import numpy as np
import os
import sys
import platform
import tensorflow as tf
from sklearn import metrics
import numpy as np
import pandas as pd
import sklearn
from imblearn.over_sampling import BorderlineSMOTE
from sklearn.model_selection import KFold

from src.classification.read_and_split_data import get_and_split_data

o_path = os.getcwd()
sys.path.append(o_path)
sys.path.append("../")
sys.path.append(os.path.join(str(o_path), "character_recognition"))


def cnn(project, K=5):
    epoch = 20
    batch_size = 64
    label_threshold = 0.5
    if platform.system() == "Windows":
        check_path = ".\\tmp\\checkpoint"
        summary_path = ".\\tmp\\summary"
        model_name = ".\\character_recognition\\save_model"

    else:
        check_path = "./tmp/checkpoint"
        summary_path = "./tmp/summary"
        model_name = "./character_recognition/save_model"
    lr = 0.001

    project = 'caffe'

    data_path = r"E:\opensource\Indirect Dependency\indirect-dependency\subspace\classification\dataset\{}.csv".format(
        project)

    train_X, train_Y, test_X, test_Y = get_and_split_data(data_path, K)
    AUC = 0
    ACC = 0
    F1 = 0
    result = []

    for i in range(K):
        train_data, train_label, test_data, test_label = train_X[i], train_Y[i], test_X[i], test_Y[i]
        train_x, train_y, test_x, test_y = train_data, train_label, test_data, test_label
        train_data = train_data.reshape(train_data.shape[0], train_data.shape[1], 1)
        test_data = test_data.reshape(test_data.shape[0], test_data.shape[1], 1)

        print("*" * 150)
        print("Input data shape:")
        print("train data:", train_data.shape, train_label.shape)
        print("test data:", test_data.shape, test_label.shape)
        print("*" * 150)

        model = tf.keras.models.Sequential(
            [
                tf.keras.layers.Conv1D(16, 4, activation="relu", input_shape=(128, 1)),
                tf.keras.layers.MaxPooling1D(3, 3),
                tf.keras.layers.Conv1D(32, 4, activation="relu"),
                tf.keras.layers.MaxPooling1D(3, 3),
                tf.keras.layers.Flatten(),
                tf.keras.layers.Dense(128, activation=tf.nn.relu),
                tf.keras.layers.Dense(64, activation=tf.nn.relu),
                tf.keras.layers.Dense(1, activation=tf.nn.sigmoid),
            ]
        )

        model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
        model.summary()

        history = model.fit(train_data, train_label, epochs=epoch, batch_size=batch_size)

        start_time = time.time()
        loss, accu = model.evaluate(test_data, test_label, verbose=0)
        print("*" * 100)
        print("loss:", loss, "accu:", accu)
        float_arr = test_data.astype(np.float16)
        raw_scores = model.predict(float_arr)
        pred = np.where(raw_scores > label_threshold, 1, 0)
        end_time = time.time()
        use_time = end_time - start_time
        pred = pred.reshape(
            pred.shape[0],
        )

        predict = pred
        precision = metrics.precision_score(test_y, predict)
        recall = metrics.recall_score(test_y, predict)
        accuracy = metrics.accuracy_score(test_y, predict)
        f1 = metrics.f1_score(test_y, predict)
        auc_score = metrics.roc_auc_score(test_y, predict)

        print(auc_score, accuracy, f1)

        if auc_score > AUC:
            AUC, ACC, F1 = auc_score, accuracy, f1
    print('auc_score %.2f%%' % (100 * AUC))
    print('accuracy: %.2f%%' % (100 * ACC))
    print('F1 %.2f%%' % (100 * F1))

    result.append(AUC)
    result.append(ACC)
    result.append(F1)

    return result


if __name__ == '__main__':
    projects = ['Caffe', 'Keras', 'Pytorch', 'Tensorflow', 'Theano']
    data = []
    for project in projects[:]:
        data.append(cnn(project))

    print(data)
    result = np.array(data).T

    with open('classify_cnn_result.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for row in result:
            writer.writerow(row)
