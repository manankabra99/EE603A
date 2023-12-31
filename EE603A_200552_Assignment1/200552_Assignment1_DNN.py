# -*- coding: utf-8 -*-
"""MLSP.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/189YrDX9ehkdsT91-EaawSGOvuxkx1pDm
"""

import tensorflow as tf
from tensorflow.keras import layers
import pandas as pd
import numpy as np
import sklearn
import os
from tensorflow.keras import datasets, layers, models
from tensorflow.keras.utils import to_categorical
from keras.callbacks import TensorBoard
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from sklearn.metrics import mean_squared_error
from math import sqrt

dataFile = "/content/drive/MyDrive/MLSP/annotations.csv"

df = pd.read_csv(dataFile)
df.head()

DX = df.iloc[:,1].values
y = df.iloc[:,2].values
print(DX[1:5])

path = '/content/drive/MyDrive/MLSP/train'
os.chdir(path)
X = os.listdir()
for i in range(len(X)):
  X[i] = np.load(X[i])
print(len(X))
print(X[0])

mx = 0
for i in X:
  mx = max(mx, i.shape[2])
print(mx)
for i in range(len(X)):
  X[i] = X[i].reshape(X[i].shape[1], X[i].shape[2])
  X[i] = np.pad(X[i], ((0,0),(0,mx-X[i].shape[1])), 'constant', constant_values = (0))
  X[i] = X[i].reshape(1, X[i].shape[0], X[i].shape[1])

print(X[0].shape)

from sklearn.preprocessing import LabelEncoder
encoder =  LabelEncoder()
y1 = encoder.fit_transform(y)

Y = pd.get_dummies(y1).values
#print(Y[0:5])

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)
print(y_train.shape)
print(X_train[0].shape)

model = tf.keras.Sequential([
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(400, activation='relu'),
    tf.keras.layers.Dense(200, activation='relu'),
    #tf.keras.layers.Dense(50, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
  ])
model

model.compile(optimizer='rmsprop', 
              loss='categorical_crossentropy',
              metrics=['accuracy'])
model.build((None,1,128,2584))
model.summary()

X_temp = X_train
X_train = tf.convert_to_tensor(X_train)
print(type(X_train))
print(type(y_train))

model.fit(X_train, y_train, batch_size=80, epochs=50)

path = '/content/drive/MyDrive/MLSP/test'
os.chdir(path)
Xt = os.listdir()
for i in range(len(Xt)):
  Xt[i] = np.load(Xt[i])

mxt = 0
for i in Xt:
  mxt = max(mxt, i.shape[2])
print(mxt)
for i in range(len(Xt)):
  Xt[i] = Xt[i].reshape(Xt[i].shape[1], Xt[i].shape[2])
  Xt[i] = np.pad(Xt[i], ((0,0),(0,mx-Xt[i].shape[1])), 'constant', constant_values = (0))
  Xt[i] = Xt[i].reshape(1, Xt[i].shape[0], Xt[i].shape[1])

Xt= tf.convert_to_tensor(Xt)

pred = model.predict(Xt)
print(pred[0])
#Xt["prediciton"] = pred
#Xt.to_csv("200552.csv")
pdf = pd.DataFrame(pred)
pdf.to_csv('200552.csv')
!cp 200552.csv "/content/drive/MyDrive/MLSP"
#pred.to_file('data2.csv', sep = ',')

#model.fit(X_train, y_train, batch_size=10, epochs=200)

#from sklearn.neighbors import KNeighborsRegressor
#print(X_temp.shape)
#print(X[0])
#X_temp = X_temp.reshape(X_temp.shape[1]*X_temp.shape[0],)
#knn_wala_model = KNeighborsRegressor(n_neighbors=10)
#knn_wala_model.fit(X_train, y_train)

#from sklearn.metrics import mean_squared_error
#from math import sqrt
#predictions = knn_wala_model.predict(X_train)
#msqerr = mean_squared_error(y_train, predictions)
#rmsqerr = sqrt(msqerr)

