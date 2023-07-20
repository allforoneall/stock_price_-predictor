
import pandas_datareader as pdr
import math
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense,LSTM
import matplotlib.pyplot as plt
import yfinance as yf

plt.style.use('fivethirtyeight')

his=yf.Ticker('AAPL')
df=his.history(start='2021-04-17',end='2023-05-28',auto_adjust='True')
df


df.shape

plt.figure(figsize=(16,8))
plt.title('close price history')

plt.plot(df['Close'])
plt.xlabel('Date',fontsize=18)
plt.ylabel('Close price',fontsize=18)
plt.show()

data=df.filter(['Close'])
dataset=data.values
training_data_len=math.ceil( len(dataset)* .8)
training_data_len

scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(dataset)
scaled_data

train_data = scaled_data[0:training_data_len,:]
x_train = []
y_train = []
for i in range(60,len(train_data)):
  x_train.append(train_data[i-60:i,0])
  y_train.append(train_data[i,0])
  if i<=61:
    print(x_train)
    print(y_train)
    print()

x_train, y_train = np.array(x_train),np.array(y_train)

x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))
x_train.shape

model = Sequential()
model.add(LSTM(50,return_sequences = True, input_shape =(x_train.shape[1],1)))
model.add(LSTM(50,return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))

model.compile(optimizer = 'adam',loss= 'mean_squared_error')

model.fit(x_train,y_train,batch_size=1,epochs=50)

test_data = scaled_data[training_data_len-60: , :]
x_test = []
y_test = dataset[training_data_len:, :]
for i in range(60, len(test_data)):
  x_test.append(test_data[i-60:i,0])

x_test = np.array(x_test)

x_test = np.reshape(x_test, (x_test.shape[0],x_test.shape[1],1))

prediction = model.predict(x_test)
prediction = scaler.inverse_transform(prediction)

rmse = np.sqrt(np.mean(prediction - y_test)**2)
rmse

train = data[: training_data_len]
valid = data[training_data_len:]
valid['prediction'] = prediction
plt.figure(figsize=(16,8))
plt.title('model')
plt.xlabel('Date',fontsize=18)
plt.ylabel('Close price',fontsize=18)
plt.plot(train['Close'])
plt.plot(valid[['Close','prediction']])
plt.legend(['Train', 'Val', 'Prediction'],loc='lower right')

plt.show

valid

his=yf.Ticker('AAPL')
apple_quote=his.history(start='2021-04-17',end='2023-05-24',auto_adjust='True')

new_df = apple_quote.filter(['Close'])
last_60_days= new_df[-60:].values
last_60_days_scaled= scaler.transform(last_60_days)
X_test = []
X_test.append(last_60_days_scaled)
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

pred_price=model.predict(X_test)
pred_price = scaler.inverse_transform(pred_price)
print(pred_price)

