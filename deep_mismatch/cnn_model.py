import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F


class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=5, stride=1, padding=1)
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=16, kernel_size=3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(in_channels=16, out_channels=4, kernel_size=3, stride=1, padding=1)
        self.fc1 = nn.Linear(6976, 1024)
        self.fc2 = nn.Linear(1024, 6)
    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

def reshape(df):
    df_values = df.values
    reshaped_data = []
    for row in df_values:
        reshaped_row = row.reshape(-1, 10, 10)
        reshaped_row = np.concatenate(reshaped_row, axis=1)
        reshaped_data.append(reshaped_row)
    reshaped_data = np.stack(reshaped_data)
    reshaped_data = reshaped_data[:, np.newaxis, :, :]
    return reshaped_data

def pre_process_data(all1st_final_vectors):
    res_df = pd.DataFrame()
    pair_names = []
    for key, value in all1st_final_vectors.items():
        f = 0
        concatenated_array = []
        for inner_key, inner_value in value.items():
            for array_key, array_value in inner_value.items():
                if f == 0:
                    pair_names.append(array_key)
                    f = 1
                concatenated_array.append(array_value)
        concatenated_array = np.concatenate(concatenated_array)
        res_df[key] = concatenated_array
    res_df = res_df.T
    res_df = reshape(res_df)
    X = torch.tensor(res_df, dtype=torch.float32)
    return (X, pair_names)
