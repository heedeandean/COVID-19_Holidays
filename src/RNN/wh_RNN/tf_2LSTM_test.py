'''
This script shows how to predict stock prices using a basic RNN
'''
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler as scaler
from varname import nameof


def MinMaxScaler(data):
    ''' Min Max Normalization
    Parameters
    ----------
    data : numpy.ndarray
        input data to be normalized
        shape: [Batch size, dimension]
    Returns
    ----------
    data : numpy.ndarry
        normalized data
        shape: [Batch size, dimension]
    References
    ----------
    .. [1] http://sebastianraschka.com/Articles/2014_about_feature_scaling.html
    '''
    numerator = data - np.min(data, 0)
    denominator = np.max(data, 0) - np.min(data, 0)
    # noise term prevents the zero division
    return numerator / (denominator + 1e-7)


# train Parameters
seq_length = 5
data_dim = 3
output_dim = 1
learning_rate = 0.003
iterations = 1000

# Open, High, Low, Volume, Close
xy = pd.read_csv('test_kk.csv')

del xy['date']
xy = xy.values[1:].astype(np.float)

xy = xy[::-1]  # reverse order (chronically ordered)

# train/test split
train_size = int(len(xy) * 0.7)
train_set = xy[0:train_size]
test_set = xy[train_size - seq_length:]  # Index from [train_size - seq_length] to utilize past sequence

min_max_x = scaler()
min_max_y = scaler()

min_max_x_fit = min_max_x.fit(xy[:,:-1])
min_max_y_fit = min_max_y.fit(xy[:,[-1]])

train_set_sc_x = min_max_x.transform(train_set[:, :-1])
train_set_sc_y = min_max_y.transform(train_set[:, [-1]])
test_set_sc_x = min_max_x.transform(test_set[:, :-1])
test_set_sc_y = min_max_y.transform(test_set[:, [-1]])

train_set = np.concatenate((train_set_sc_x,train_set_sc_y), axis=1)
test_set = np.concatenate((test_set_sc_x,test_set_sc_y), axis=1)

# build datasets
def build_dataset(time_series, seq_length):
    dataX = []
    dataY = []
    for i in range(0, len(time_series) - seq_length):
        print('{}번째'.format(i))
        x = time_series[i:i + seq_length, :-1]
        y = time_series[i + seq_length, [-1]]  # Next close price
        print(x, "->", y)
        dataX.append(x)
        dataY.append(y)
        print('-'*10)
    return np.array(dataX), np.array(dataY)


trainX, trainY = build_dataset(train_set, seq_length)
testX, testY = build_dataset(test_set, seq_length)

print(trainX.shape)
print(testX.shape)
print(trainY.shape)
print(testY.shape)


tf.model = tf.keras.Sequential()
tf.model.add(tf.keras.layers.LSTM(units=1, input_shape=(seq_length, data_dim)))
tf.model.add(tf.keras.layers.Dense(units=output_dim, activation='tanh'))
tf.model.summary()


tf.model.compile(loss='mse',
                 optimizer=tf.keras.optimizers.Adam(lr=learning_rate),
                 # optimizer='adam',
                 metrics=['accuracy'])
tf.model.fit(trainX, trainY, epochs=iterations)

# Test step
test_predict = tf.model.predict(testX)

# Plot predictions
plt.plot(min_max_y.inverse_transform(testY))
plt.plot(min_max_y.inverse_transform(test_predict))
plt.xlabel("Time Period")
plt.ylabel("Stock Price")
plt.show()
