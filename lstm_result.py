# -*- coding: utf-8 -*-
"""csci3391_project_LSTM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1U3dqmKtFUtzXhEd2u9OYs2d1nK13a2RK
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json

# df = pd.read_csv('SBUX.csv', index_col = 'Date', parse_dates=True)

"""# load data"""

path='/content/mastodon2.json'
with open(path) as json_data:
   obj = json.load(json_data)
  #  print(obj)
   df_m = pd.DataFrame(obj['data']['platforms'][0]['statSet'], columns=['date','usersMonthly','usersTotal'])

df_m['date'] = pd.to_datetime(df_m['date'])
df_m=df_m.sort_values(by='date')

mask=df_m['date']>'2021-12-31'
df_m=df_m.loc[mask].reset_index(drop=True)

Nov_interval = ('2022-10-21','2022-11-21')
mask1=(df_m['date'] >= Nov_interval[0]) & (df_m['date'] <= Nov_interval[1])
df1 = df_m.loc[mask1].reset_index(drop=True)
df1['Diff'] = df1['usersTotal'].diff()
df1.at[0,'Diff']=0
# df1['label']=df1['Diff'].shift(periods=7,fill_value=0)

d=df1["Diff"].to_numpy()
len_x = 7
len_y = 7
width = len_x + len_y
thing = [d[i:] for i in range(width)]
# print(thing)
min_length = min(len(x) for x in thing)
thing = [x[:min_length] for x in thing]
thing = np.stack(thing, axis=1)
# print(thing)
data = thing[:, :len_x]
target = thing[:, len_x:]
# print()
print(data.shape)
print(target.shape)

"""# plot features(new infections)"""

plt.style.use('ggplot')
plt.plot(df1['Diff'],label='New Infections')
plt.legend()
plt.show()

X = data.copy() 
y = target.copy()

from sklearn.preprocessing import StandardScaler, MinMaxScaler
mm = MinMaxScaler()
ss = StandardScaler()

X_ss = ss.fit_transform(X)
y_mm = mm.fit_transform(y)

X_ss.shape  #minmax scalar for each column

# for training

X_train = X_ss[:, :]
# X_test = X_ss[21:, :]

y_train = y_mm[:, :]
# y_test = y_mm[21:, :] 
print("Training Shape", X_train.shape, y_train.shape)
# print("Testing Shape", X_test.shape, y_test.shape)

"""# LSTM"""

import torch #pytorch
import torch.nn as nn
from torch.autograd import Variable

X_train_tensors = Variable(torch.Tensor(X_train))
# X_test_tensors = Variable(torch.Tensor(X_test))

y_train_tensors = Variable(torch.Tensor(y_train))
# y_test_tensors = Variable(torch.Tensor(y_test))

X_train_tensors.shape

#reshaping to rows, timestamps, features

X_train_tensors_final = torch.reshape(X_train_tensors,   (X_train_tensors.shape[0], 1, X_train_tensors.shape[1]))

# X_test_tensors_final = torch.reshape(X_test_tensors,  (X_test_tensors.shape[0], 1, X_test_tensors.shape[1]))

X_train_tensors_final.shape

class LSTM1(nn.Module):
    def __init__(self, num_classes, input_size, hidden_size, num_layers, seq_length):
        super(LSTM1, self).__init__()
        self.num_classes = num_classes #number of classes
        self.num_layers = num_layers #number of layers
        self.input_size = input_size #input size
        self.hidden_size = hidden_size #hidden state
        self.seq_length = seq_length #sequence length

        self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size,
                          num_layers=num_layers, batch_first=True) #lstm
        self.fc_1 =  nn.Linear(hidden_size, 128) #fully connected 1
        self.fc = nn.Linear(128, num_classes) #fully connected last layer

        self.relu = nn.ReLU()
    
    def forward(self,x):
        h_0 = Variable(torch.zeros(self.num_layers, x.size(0), self.hidden_size)) #hidden state
        c_0 = Variable(torch.zeros(self.num_layers, x.size(0), self.hidden_size)) #internal state
        # Propagate input through LSTM
        output, (hn, cn) = self.lstm(x, (h_0, c_0)) #lstm with input, hidden, and internal state
        hn = hn.view(-1, self.hidden_size) #reshaping the data for Dense layer next
        out = self.relu(hn)
        out = self.fc_1(out) #first Dense
        out = self.relu(out) #relu
        out = self.fc(out) #Final Output
        return out

num_epochs = 1000 #1000 epochs
learning_rate = 0.001 #0.001 lr

input_size = 7 #number of features
hidden_size = 2 #number of features in hidden state
num_layers = 1 #number of stacked lstm layers

num_classes = 7 #number of output classes

lstm1 = LSTM1(num_classes, input_size, hidden_size, num_layers, X_train_tensors_final.shape[1]) #our lstm class

criterion = torch.nn.MSELoss()    # mean-squared error for regression
optimizer = torch.optim.Adam(lstm1.parameters(), lr=learning_rate)

for epoch in range(num_epochs):
  outputs = lstm1.forward(X_train_tensors_final) #forward pass
  optimizer.zero_grad() #caluclate the gradient, manually setting to 0
 
  # obtain the loss function
  loss = criterion(outputs, y_train_tensors)
 
  loss.backward() #calculates the loss of the loss function
 
  optimizer.step() #improve from loss, i.e backprop
  if epoch % 100 == 0:
    print("Epoch: %d, loss: %1.5f" % (epoch, loss.item()))

# generate test data
input=df1.iloc[:, 3:4][-7:].to_numpy().reshape(1,-1)
# print(input.shape)
df_X_ss = ss.fit_transform(input) #old transformers
print(df_X_ss.shape)
df_y_mm = mm.fit_transform(df1.iloc[:, -1:]) #old transformers
print(df_y_mm.shape)

df_X_ss = Variable(torch.Tensor(df_X_ss)) #converting to Tensors
df_y_mm = Variable(torch.Tensor(df_y_mm)) 

#reshaping the dataset
df_X_ss = torch.reshape(df_X_ss, (df_X_ss.shape[0], 1, df_X_ss.shape[1]))

train_predict = lstm1(df_X_ss)  #forward pass
data_predict = train_predict.data.numpy() #numpy conversion
dataY_plot = df_y_mm.data.numpy()

data_predict = mm.inverse_transform(data_predict) #reverse transformation
# print(data_predict.flatten().shape)

zero_pad=np.empty((df_y_mm.shape[0]-1+7,))
# print(zero_pad.shape)
zero_pad.fill(np.NaN)
zero_pad[-7:]=data_predict
# print(zero_pad)

dataY_plot = mm.inverse_transform(dataY_plot)

# dataY_plot = dataY_plot.flatten().tolist()
# print(type(dataY_plot))
# lst1=[]
# for i in range(7):
#   lst1.append(0)
# print(lst1)

plt.figure(figsize=(12,6)) #plotting
plt.title('Prediction of next 7 days')
plt.axvline(x=df_y_mm.shape[0]-1, c='black', linestyle='--') #size of the training set

plt.plot(dataY_plot, label='Actual') #actual plot
plt.plot(zero_pad, label='Predicted') #predicted plot
# plt.title('Time-Series Prediction')
plt.legend()
plt.show()

