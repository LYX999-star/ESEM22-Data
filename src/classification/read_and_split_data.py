import numpy as np
import pandas as pd
import sklearn
from imblearn.over_sampling import BorderlineSMOTE
from sklearn.model_selection import KFold


def read_csv_data(data_path):
    datas = pd.read_csv(data_path, header=None)
    datas = np.array(datas)
    X_data = datas[:, :-1]
    labels = datas[:, -1:].reshape(-1)

    y_label = []
    for label in labels:
        if label == True:
            y_label.append(1)
        else:
            y_label.append(0)

    X_data, y_label = X_data, np.array(y_label)

    X_resampled, y_resampled = sm = BorderlineSMOTE(random_state=42,kind="borderline-1").fit_resample(X_data, y_label)

    return X_resampled, y_resampled


def get_and_split_data(data_path, k):
    X_data, y_label = read_csv_data(data_path)
    X_data, y_label = sklearn.utils.shuffle(X_data, y_label)

    train_x, train_y, test_x, test_y = [], [], [], []

    kf = KFold(n_splits=k, shuffle=True)

    for train_index, test_index in kf.split(X_data):
        train_x.append(X_data[train_index])
        train_y.append(y_label[train_index])
        test_x.append(X_data[test_index])
        test_y.append(y_label[test_index])

    return train_x, train_y, test_x, test_y


if __name__ == '__main__':
    data_path = r"E:\opensource\Indirect Dependency\indirect-dependency\subspace\classification\CNN\data\CS_LN.csv"
    X = np.arange(24).reshape(12, 2)
    y = np.random.choice([1, 2], 12, p=[0.4, 0.6])
    kf = KFold(n_splits=5, shuffle=False)
    for train_index, test_index in kf.split(X):
        print(train_index, test_index)
