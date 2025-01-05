import sys

sys.path.append("..")

import logging

import bentoml
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor

from config.logging_config import setup_logging
from utils.timescale_connector import TimescaleConnector

setup_logging()


symbol_lts = TimescaleConnector.get_symbols()

df_ = {}
for symbol in symbol_lts:
    df_[symbol] = TimescaleConnector.query_ohlcv_daily(symbol)


# Prices prior to 2023 as a training set and the rest as test set
def split(dataframe, border, col):
    return dataframe.loc[:border, col], dataframe.loc[border:, col]


df_new = {}
for stock in symbol_lts:
    df_new[stock] = {}
    df_new[stock]["Train"], df_new[stock]["Test"] = split(df_[stock], "2023", "close")


# Scaling the training set
transform_train = {}
transform_test = {}
scaler = {}

for num, i in enumerate(symbol_lts):
    sc = MinMaxScaler(feature_range=(0, 1))
    a0 = np.array(df_new[i]["Train"])
    a1 = np.array(df_new[i]["Test"])
    a0 = a0.reshape(a0.shape[0], 1)
    a1 = a1.reshape(a1.shape[0], 1)
    transform_train[i] = sc.fit_transform(a0)
    transform_test[i] = sc.fit_transform(a1)
    scaler[i] = sc

del a0
del a1


for i in transform_train.keys():
    logging.info(i, transform_train[i].shape)
logging.info("\n")
for i in transform_test.keys():
    logging.info(i, transform_test[i].shape)


# Check the average length of the training set
length = []
for i in transform_train.keys():
    length.append(transform_train[i].shape[0])
logging.info("Average length of the training set: ", np.mean(length))


keys_to_delete = []
for i in transform_train.keys():
    if transform_train[i].shape[0] < 1400:
        keys_to_delete.append(i)

for key in keys_to_delete:
    del transform_train[key]
    del transform_test[key]
    del scaler[key]

# Create a new symbol list from the training set
symbol_lst_filtered = []
for i in transform_train.keys():
    symbol_lst_filtered.append(i)


trainset = {}
testset = {}
for j in symbol_lst_filtered:
    trainset[j] = {}
    X_train = []
    y_train = []
    for i in range(60, 1400):
        X_train.append(transform_train[j][i - 60 : i, 0])
        y_train.append(transform_train[j][i, 0])
    X_train, y_train = np.array(X_train), np.array(y_train)
    trainset[j]["X"] = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
    trainset[j]["y"] = y_train

    testset[j] = {}
    X_test = []
    y_test = []
    for i in range(60, 226):
        X_test.append(transform_test[j][i - 60 : i, 0])
        y_test.append(transform_test[j][i, 0])
    X_test, y_test = np.array(X_test), np.array(y_test)
    testset[j]["X"] = np.reshape(X_test, (X_test.shape[0], X_train.shape[1], 1))
    testset[j]["y"] = y_test


# CHeck the training set again before training
arr_buff = []
for i in symbol_lst_filtered:
    buff = {}
    buff["X_train"] = trainset[i]["X"].shape
    buff["y_train"] = trainset[i]["y"].shape
    buff["X_test"] = testset[i]["X"].shape
    buff["y_test"] = testset[i]["y"].shape
    arr_buff.append(buff)

pd.DataFrame(arr_buff, index=symbol_lst_filtered)


device = "cuda:0" if torch.cuda.is_available() else "cpu"
device


X_test.shape


# Transform numpy arrays to tensors
X_train = torch.tensor(X_train).float()
y_train = torch.tensor(y_train).float()
X_test = torch.tensor(X_test).float()
y_test = torch.tensor(y_test).float()


for i in symbol_lst_filtered:
    logging.info("Fitting to", i)
    logging.info(trainset[i]["X"], trainset[i]["y"])


# Create a DataLoader
# Assuming that data_dict is a dictionary where
# the key is the stock name and the value is a tuple of (features, labels)
from torch.utils.data import TensorDataset

train_loaders = {}

for stock in symbol_lst_filtered:
    # Convert numpy arrays to PyTorch tensors
    features_tensor = torch.tensor(trainset[i]["X"]).float()
    labels_tensor = torch.tensor(trainset[i]["y"]).float()

    # Create a TensorDataset from the tensors
    dataset = TensorDataset(features_tensor, labels_tensor)

    # Create a DataLoader from the TensorDataset
    train_loader = DataLoader(dataset, batch_size=200, shuffle=True)

    # Add the DataLoader to the dictionary
    train_loaders[stock] = train_loader


# Create test sets
test_loaders = {}

for stock in symbol_lst_filtered:
    # Convert numpy arrays to PyTorch tensors
    features_tensor = torch.tensor(testset[i]["X"]).float()
    labels_tensor = torch.tensor(testset[i]["y"]).float()

    # Create a TensorDataset from the tensors
    dataset = TensorDataset(features_tensor, labels_tensor)

    # Create a DataLoader from the TensorDataset
    test_loader = DataLoader(dataset, batch_size=200, shuffle=True)

    # Add the DataLoader to the dictionary
    test_loaders[stock] = test_loader


# Create a LSTM class
class LSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_stacked_layers):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_stacked_layers = num_stacked_layers
        self.lstm = nn.LSTM(
            input_size, hidden_size, num_stacked_layers, batch_first=True
        )
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        batch_size = x.size(0)
        h0 = torch.zeros(self.num_stacked_layers, batch_size, self.hidden_size).to(
            device
        )
        c0 = torch.zeros(self.num_stacked_layers, batch_size, self.hidden_size).to(
            device
        )
        # We need to detach as we are doing truncated backpropagation through time (BPTT)
        out, (hn, cn) = self.lstm(x, (h0.detach(), c0.detach()))
        out = self.fc(out[:, -1, :])
        return out


model = LSTM(1, 6, 1)
model.to(device)


def train_one_epoch():
    model.train(True)
    for i in symbol_lst_filtered:
        logging("Fitting to", i)
        running_loss = 0.0
        for epoch in range(num_epochs):
            logging.info(f"Epoch: {epoch + 1}")
            for batch_index, batch in enumerate(train_loaders[i]):
                x_batch, y_batch = batch[0].to(device), batch[1].to(device)

                output = model(x_batch).squeeze()
                loss = loss_function(output, y_batch)
                running_loss += loss.item()

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                if batch_index % 100 == 99:  # logging.info every 100 batches
                    avg_loss_across_batches = running_loss / 100
                    logging.info(
                        "Batch {0}, Loss: {1:.3f}".format(
                            batch_index + 1, avg_loss_across_batches
                        )
                    )
                    running_loss = 0.0
            logging.info()


def validate_one_epoch():
    model.train(False)
    running_loss = 0.0
    for stock in symbol_lst_filtered:
        for batch_index, batch in enumerate(test_loaders[stock]):
            x_batch, y_batch = batch[0].to(device), batch[1].to(device)

            with torch.no_grad():
                output = model(x_batch).squeeze()
                loss = loss_function(output, y_batch)
                running_loss += loss.item()

    avg_loss_across_batches = running_loss / len(test_loaders)

    logging.info("Val Loss: {0:.3f}".format(avg_loss_across_batches))


if __name__ == "__main__":
    setup_logging()
    model = LSTM(1, 6, 1)
    model.to(device)
    learning_rate = 0.001
    num_epochs = 10
    loss_function = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    for epoch in range(num_epochs):
        train_one_epoch()
        validate_one_epoch()

    # Save the model
    torch.save(model.state_dict(), "model.pt")
    bentoml.pytorch.save_model(model, "LSTM-Stock-Prediction")

# Predict the test
# from sklearn.metrics import mean_squared_error

# pred_result = {}
# for i in symbol_lst_filtered[:5]:
#     y_true = scaler[i].inverse_transform(torch.tensor(testset[i]["y"]).float().reshape(-1, 1))
#     y_pred = scaler[i].inverse_transform(
#         model(torch.tensor(testset[i]["X"]).float().to(device)).detach().cpu().numpy()
#     )
#     MSE = mean_squared_error(y_true, y_pred)
#     pred_result[i] = {}
#     pred_result[i]["True"] = y_true
#     pred_result[i]["Pred"] = y_pred

#     plt.figure(figsize=(14, 6))
#     plt.title("{} with MSE {:10.4f}".format(i, MSE))
#     plt.plot(y_true, label='Actual Close')
#     plt.plot(y_pred, label='Predicted Close')
#     plt.legend()
#     plt.show()
