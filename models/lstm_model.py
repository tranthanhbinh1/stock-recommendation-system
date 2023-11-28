import torch
import logging
from torch import nn
from torch.utils.data import DataLoader, Dataset

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from copy import deepcopy as dc
from utils.timescale_connector import TimescaleConnector
from config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

data = TimescaleConnector.query_ohlcv_daily("ACB")
device = "cuda:0" if torch.cuda.is_available() else "cpu"

data = data[["date", "close"]]


def prepare_dataframe_for_lstm(df, n_steps):
    df = dc(df)

    df.set_index("date", inplace=True)
    for i in range(1, n_steps + 1):
        df[f"close(t-{i})"] = df["close"].shift(i)
    df.dropna(inplace=True)

    return df


# Prepare the data for LSTM
class LSTMDataPrep:
    lookback = 5
    shifted_df = prepare_dataframe_for_lstm(data, lookback)

    # Transform to numpy arrays
    shifted_df_as_np = shifted_df.to_numpy()
    # scale the data to range from -1 to 1, matched the range of the tanh activation function
    scaler = MinMaxScaler(feature_range=(-1, 1))
    shifted_df_as_np = scaler.fit_transform(shifted_df_as_np)
    X = shifted_df_as_np[:, 1:]  # input features
    y = shifted_df_as_np[:, 0]  # target feature
    # Train test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05, shuffle=False)
    # Reshaping the data to add an extra dimension for PyTorch lstm
    X_train = X_train.reshape((-1, lookback, 1))
    X_test = X_test.reshape((-1, lookback, 1))
    y_train = y_train.reshape((-1, 1))
    y_test = y_test.reshape((-1, 1))
    # Transform numpy arrays to tensors
    X_train = torch.tensor(X_train).float()
    y_train = torch.tensor(y_train).float()
    X_test = torch.tensor(X_test).float()
    y_test = torch.tensor(y_test).float()


# Create a dataset for torch
class TimeSeriesDataset(Dataset):
    def __init__(self, X, y):
        self.X = X
        self.y = y

    def __len__(self):
        return len(self.X)

    def __getitem__(self, i):
        return self.X[i], self.y[i]


train_dataset = TimeSeriesDataset(X_train, y_train)
test_dataset = TimeSeriesDataset(X_test, y_test)

# Create a DataLoader
batch_size = 10
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)


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

        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out


model = LSTM(1, 6, 1)
model.to(device)


# Train function
def train_one_epoch():
    model.train(True)
    logger.info(f"Epoch: {epoch + 1}")
    running_loss = 0.0

    for batch_index, batch in enumerate(train_loader):
        x_batch, y_batch = batch[0].to(device), batch[1].to(device)

        output = model(x_batch)
        loss = loss_function(output, y_batch)
        running_loss += loss.item()

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if batch_index % 100 == 99:  # print every 100 batches
            avg_loss_across_batches = running_loss / 100
            logger.info(
                "Batch {0}, Loss: {1:.3f}".format(
                    batch_index + 1, avg_loss_across_batches
                )
            )
            running_loss = 0.0


def validate_one_epoch():
    model.train(False)
    running_loss = 0.0

    for batch_index, batch in enumerate(test_loader):
        x_batch, y_batch = batch[0].to(device), batch[1].to(device)

        with torch.no_grad():
            output = model(x_batch)
            loss = loss_function(output, y_batch)
            running_loss += loss.item()

    avg_loss_across_batches = running_loss / len(test_loader)

    print("Val Loss: {0:.3f}".format(avg_loss_across_batches))
    print("***************************************************")


if __name__ == "__main__":
    learning_rate = 0.01
    num_epochs = 30
    loss_function = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    for epoch in range(num_epochs):
        train_one_epoch()
        validate_one_epoch()
