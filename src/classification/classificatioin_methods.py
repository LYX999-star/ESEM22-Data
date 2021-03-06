# coding=gbk
import csv
import time

import numpy as np
from sklearn import metrics
import pickle as pickle
import pandas as pd
from src.classification.read_and_split_data import get_and_split_data


# Multinomial Naive Bayes Classifier
def naive_bayes_classifier(train_x, train_y):
    from sklearn.naive_bayes import GaussianNB
    model = GaussianNB()
    model.fit(train_x, train_y)
    return model


# KNN Classifier
def knn_classifier(train_x, train_y):
    from sklearn.neighbors import KNeighborsClassifier
    model = KNeighborsClassifier()
    model.fit(train_x, train_y)
    return model


# Logistic Regression Classifier
def logistic_regression_classifier(train_x, train_y):
    from sklearn.linear_model import LogisticRegression
    model = LogisticRegression(penalty='l2')
    model.fit(train_x, train_y)
    return model


# Random Forest Classifier
def random_forest_classifier(train_x, train_y):
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(n_estimators=220, min_samples_leaf=10, min_samples_split=30, max_depth=8,
                                   random_state=10,
                                   criterion='gini', class_weight=None)
    model.fit(train_x, train_y)
    return model


# Decision Tree Classifier
def decision_tree_classifier(train_x, train_y):
    from sklearn import tree
    model = tree.DecisionTreeClassifier()
    model.fit(train_x, train_y)
    return model


# GBDT(Gradient Boosting Decision Tree) Classifier
def gradient_boosting_classifier(train_x, train_y):
    from sklearn.ensemble import GradientBoostingClassifier
    model = GradientBoostingClassifier(n_estimators=200)
    model.fit(train_x, train_y)
    return model


# XGB(XGBoost) Classifier
def XGBoost_classifier(train_x, train_y):
    from xgboost import XGBClassifier
    model = XGBClassifier(learning_rate=0.1, n_estimators=100, max_depth=9, min_child_weight=1,
                          subsample=0.6, colsample_bytree=0.8, gamma=0.4, reg_alpha=1, reg_lambda=0.01)
    model.fit(train_x, train_y)
    return model


# SVM Classifier
def svm_classifier(train_x, train_y):
    from sklearn.svm import SVC
    model = SVC(kernel='rbf', probability=True)
    model.fit(train_x, train_y)
    return model


def read_data(data_file):
    data = pd.read_csv(data_file)
    train = data[:int(len(data) * 0.9)]
    test = data[int(len(data) * 0.9):]
    train_y = train.label
    train_x = train.drop('label', axis=1)
    test_y = test.label
    test_x = test.drop('label', axis=1)
    return train_x, train_y, test_x, test_y


def patch(project, K=5):
    model_save_file = None
    model_save = {}

    result = []

    test_classifiers = [
        'DT',
        'NB',
        'SVM',
        'LR',
        'RF',
        'XGB',
    ]
    classifiers = {
        'NB': naive_bayes_classifier,
        'KNN': knn_classifier,
        'LR': logistic_regression_classifier,
        'RF': random_forest_classifier,
        'DT': decision_tree_classifier,
        'SVM': svm_classifier,
        'GBDT': gradient_boosting_classifier,
        'XGB': XGBoost_classifier
    }

    print('reading training and testing data...')

    data_path = r"E:\opensource\Indirect Dependency\indirect-dependency\subspace\classification\dataset\{}.csv".format(
        project)

    train_X, train_Y, test_X, test_Y = get_and_split_data(data_path, K)

    for classifier in test_classifiers[:]:
        AUC = 0
        ACC = 0
        F1 = 0
        for i in range(K):
            train_x, train_y, test_x, test_y = train_X[i], train_Y[i], test_X[i], test_Y[i]

            print('******************* %s ********************' % classifier)
            start_time = time.time()
            model = classifiers[classifier](train_x, train_y)
            print('training took %fs!' % (time.time() - start_time))
            predict = model.predict(test_x)
            if classifier == 'XGB':
                a, b = predict.max(), predict.min()
                predict[predict > (a + b) / 2] = 1
                predict[predict <= (a + b) / 2] = 0

            if model_save_file != None:
                model_save[classifier] = model
            precision = metrics.precision_score(test_y, predict)
            recall = metrics.recall_score(test_y, predict)
            accuracy = metrics.accuracy_score(test_y, predict)
            f1 = metrics.f1_score(test_y, predict)
            auc_score = metrics.roc_auc_score(test_y, predict)

            if auc_score > AUC:
                AUC, ACC, F1 = auc_score, accuracy, f1
        print('auc_score %.2f%%' % (100 * AUC))
        print('accuracy: %.2f%%' % (100 * ACC))
        print('F1 %.2f%%' % (100 * F1))

        result.append(AUC)
        result.append(ACC)
        result.append(F1)

    if model_save_file != None:
        pickle.dump(model_save, open(model_save_file, 'wb'))

    return result


if __name__ == '__main__':
    projects = ['Caffe', 'Keras', 'Pytorch', 'Tensorflow', 'Theano']
    data = []
    for project in projects[:]:
        data.append(patch(project))

    print(data)
    result = np.array(data).T

    with open('classify_result.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for row in result:
            writer.writerow(row)
