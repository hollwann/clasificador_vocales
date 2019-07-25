# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 15:22:00 2019

@author: Hollwann

train network for vowel recognition
"""

import numpy as np
from glob import glob
from tensorflow.keras.layers import Dense, LSTM, Dropout
from tensorflow.keras.models import Sequential
from scipy.io import wavfile

db_files = glob('db/*.npy')
db_files.sort()

x = []
y = []
for file in db_files:
    f = np.load(file)
    x.append(f)
    if file[3] == "a":
        y.append(0)
    elif file[3] == "e":
        y.append(1)
    elif file[3] == "i":
        y.append(2)
    elif file[3] == "o":
        y.append(3)
    elif file[3] == "u":
        y.append(4)

x_size = sum([el.shape[0] for el in x])

train_x = np.zeros((x_size, 256))
train_y = np.zeros(x_size)

actual_idx = 0
for i in range(len(x)):
    train_x[actual_idx:actual_idx+x[i].shape[0]] = x[i]
    train_y[actual_idx:actual_idx+x[i].shape[0]].fill(y[i])
    actual_idx += x[i].shape[0]
    

def build_model():
    model = Sequential()
    
    model.add(Dense(32, activation="relu", input_shape=(256,)))
    model.add(Dropout(0.5))
    '''
    model.add(Dropout(0.2))
    model.add(Dense(128, activation="relu"))
    model.add(Dropout(0.2))
    model.add(Dense(128, activation="relu"))
    model.add(Dropout(0.2))
    model.add(Dense(128, activation="relu"))
    model.add(Dropout(0.2))
    model.add(Dense(128, activation="relu"))
    model.add(Dropout(0.2))
    model.add(Dense(128, activation="relu"))
    model.add(Dropout(0.2))
    model.add(Dense(128, activation="relu"))
    model.add(Dropout(0.2))
    model.add(Dense(128, activation="relu"))
    model.add(Dropout(0.2))'''
    model.add(Dense(5, activation='softmax'))
  
    model.compile(loss='sparse_categorical_crossentropy',
                optimizer='adam',
                metrics=['accuracy'])
    return model

model = build_model()
model.summary()
#train_x = train_x.reshape(train_x.shape[0],train_x.shape[1],1)
train_y = train_y.astype(int)
r = np.arange(train_x.shape[0])
np.random.shuffle(r)
history = model.fit(train_x[r], train_y[r], validation_split=0.3,
                    epochs=100, verbose=1, batch_size=128)

_, test_x = wavfile.read('processed/My recording 7.wav')

WINDOW = 256
STEP = 8
def gen_db(data):
    total_samples = int((len(data) - WINDOW) / STEP)
    vdb = np.zeros((total_samples, WINDOW))
    for i in range(total_samples):
        sample = data[i*8:(i*8) + WINDOW]
        if np.abs(sample).mean() > 1000:
            vdb[i] = sample
            #Se normaliza
            vdb[i] = vdb[i] / max(vdb[i].max(),1)
    vdb = vdb[~(vdb==0).all(1)]
    return vdb

test_x_d = gen_db(test_x[4800:])

a = np.argmax(model.predict(test_x_d), axis=-1)
    
    
    
    
    
    
    
    
    
    