import torch
import torch.nn as nn
from sklearn import metrics

from src.classification.read_and_split_data import get_and_split_data

x1_t = torch.normal(2 * torch.ones(100, 2), 1)
y1_t = torch.zeros(100)

x2_t = torch.normal(-2 * torch.ones(100, 2), 1)
y2_t = torch.ones(100)

x_t = torch.cat((x1_t, x2_t), 0)
y_t = torch.cat((y1_t, y2_t), 0)

project = 'caffe'

data_path = r"E:\opensource\Indirect Dependency\indirect-dependency\subspace\classification\dataset\{}.csv".format(
    project)

K = 5
train_X, train_Y, test_X, test_Y = get_and_split_data(data_path, K)
AUC = 0
ACC = 0
F1 = 0

for i in range(K):
    train_x, train_y, test_x, test_y = torch.from_numpy(train_X[i]), torch.from_numpy(train_Y[i]), torch.from_numpy(
        test_X[i]), torch.from_numpy(test_Y[i])

net = nn.Sequential(
    nn.Linear(128, 128),
    torch.nn.Sigmoid(),
    nn.Linear(128, 64),
    torch.nn.Sigmoid(),
    nn.Linear(64, 32),
    torch.nn.Sigmoid(),
    nn.Linear(32, 16),
    nn.Softmax(dim=1)
)

print(net)

optimizer = torch.optim.SGD(net.parameters(), lr=0.01)
loss_func = torch.nn.CrossEntropyLoss()

num_epoch = 5000
for epoch in range(num_epoch):
    net = net.double()

    y_p = net(train_x)

    loss = loss_func(y_p, train_y.long())

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if epoch % 1000 == 0:
        print('epoch: {}, loss: {}'.format(epoch, loss.data.item()))

predict = net(test_y)

precision = metrics.precision_score(test_y, predict)
recall = metrics.recall_score(test_y, predict)
accuracy = metrics.accuracy_score(test_y, predict)
f1 = metrics.f1_score(test_y, predict)
auc_score = metrics.roc_auc_score(test_y, predict)
print(auc_score, accuracy, f1)