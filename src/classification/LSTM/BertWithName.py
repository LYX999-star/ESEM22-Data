import numpy as np

import csv

import tensorflow as tf
from tensorflow import keras
from keras.layers import Dense, LSTM, Dropout
import keras
import keras_metrics as km
from keras.wrappers.scikit_learn import KerasClassifier
import datetime
from sklearn import metrics

from src.classification.read_and_split_data import get_and_split_data


def loadTrainset(trainset):
    X_train = []
    y_train = []
    with open(trainset) as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            a = row[0:256]
            b = []
            for i in a:
                b.append(float(i))
            X_train.append(b)
            if row[256].upper() == "TRUE":
                y_train.append(1)
            elif row[256].upper() == "FALSE":
                y_train.append(0)
    X_train = np.array(X_train)
    y_train = np.array(y_train)
    print(X_train.shape)
    print(y_train.shape)
    X_train = X_train.reshape(X_train.shape[0], 1, X_train.shape[1])
    print(X_train.shape)
    print(y_train.shape)
    return X_train, y_train


def creat_model():
    model = keras.models.Sequential()
    model.add(LSTM(64, dropout=0.2, recurrent_dropout=0.5))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer=tf.keras.optimizers.RMSprop(), loss='binary_crossentropy',
                  metrics=['acc', km.f1_score(), km.binary_precision(), km.binary_recall()])
    return model


def loadTestset(testset):
    X_test = []
    y_test = []
    labels = []
    with open(testset) as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            if (row[0] == '\x1a'):
                continue
            a = row[0:256]
            b = []
            for i in a:
                b.append(float(i))
            X_test.append(b)
            if row[256].upper() == "TRUE":
                y_test.append(1)
            elif row[256].upper() == "FALSE":
                y_test.append(0)
            label = row[257:259]
            labels.append(label)
    X_test = np.array(X_test)
    y_test = np.array(y_test)
    X_test = X_test.reshape(X_test.shape[0], 1, X_test.shape[1])
    return X_test, y_test, labels


def patch(project, K=5):
    result = []

    print('reading training and testing data...')

    data_path = r"E:\opensource\Indirect Dependency\indirect-dependency\subspace\classification\dataset\{}.csv".format(
        project)

    train_X, train_Y, test_X, test_Y = get_and_split_data(data_path, K)

    AUC = 0
    ACC = 0
    F1 = 0
    for i in range(K):
        train_x, train_y, test_x, test_y = train_X[i], train_Y[i], test_X[i], test_Y[i]

        train_x = train_x.reshape(train_x.shape[0], 1, train_x.shape[1])
        test_x = test_x.reshape(test_x.shape[0], 1, test_x.shape[1])

        model = KerasClassifier(build_fn=creat_model, verbose=1)

        batch_size = 60
        n_epochs = 100
        history = model.fit(train_x, train_y,
                            batch_size=batch_size,
                            epochs=n_epochs)

        start_time = datetime.datetime.now()
        start = start_time.strftime('%Y-%m-%d %H:%M:%S.%f')
        y_pred = model.predict(test_x, verbose=0)
        y_pred = np.int64(y_pred > 0.5)
        predict = y_pred

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
        data.append(patch(project))

    print(data)
    result = np.array(data).T

    with open('classify_LSTM_result.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for row in result:
            writer.writerow(row)
