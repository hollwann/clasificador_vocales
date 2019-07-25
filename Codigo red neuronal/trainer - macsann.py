# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 15:22:00 2019

@author: Hollwann

train network for vowel recognition
"""

import numpy as np
from glob import glob
from scipy.io import wavfile
import macsann
import pickle

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
    

r = np.arange(train_x.shape[0])
np.random.shuffle(r)
train_y = train_y[r].astype(int)
train_x = train_x[r]


if __name__ == '__main__':
     #Create macsann population
    population = macsann.population('config-example.ini')
    
    #Train data
    population.train_input = train_x[:67216]
    population.train_output = train_y[:67216]
    
    #Validation data
    population.eval_input = train_x[67216:]
    population.eval_output = train_y[67216:]
    
    #Run and get the best population
    best_pop = population.run()
    with open('best_pop.macsann','wb') as f:
        pickle.dump(best_pop, f)
        
'''
_, test_x = wavfile.read('CompadreA.wav')

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

a = np.argmax(model.predict(test_x_d), axis=-1)'''
    
    
    
    
    
    
    
    
    
    