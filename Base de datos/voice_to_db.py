# -*- coding: utf-8 -*-
"""
This file converts wav files to ready files for the network
"""

import numpy as np
from glob import glob
from scipy.io import wavfile
import matplotlib.pyplot as plt
import sys
import sounddevice as sd
import random

VOWELS = ['a', 'e', 'i', 'o', 'u']
unprocessed_files = glob('unprocessed/*.wav')
unprocessed_files.sort()
WINDOW = 256
STEP = 8

def plot_wav(data):
    plt.plot(data)
    plt.show()

def gen_db(data, vowel):
    total_samples = int((len(data) - WINDOW) / STEP)
    vdb = np.zeros((total_samples, WINDOW))
    for i in range(total_samples):
        vdb[i] = data[i*8:(i*8) + WINDOW]
        #Se normaliza
        vdb[i] = vdb[i] / max(1, vdb[i].max())
    np.save('db/' + vowel + str(random.random())[2:6], vdb)
    
def show_options(data):
    print('Por favor ingrese alguna opción:')
    print("0: para graficar el audio")
    print("1: para escuchar el audio")
    print("2: para introducir el inico y el fin deseado")
    print("3: salir")
    x = input("opcion: ")
    if x == "0": #See graph
        plot_wav(data)
        show_options(data)
    elif x == "1": #Listen
        sd.play(data, 8000)
        show_options(data)
    elif x =="2": #Save to db
        try:
            start = int(input("Muestra inicial: "))
            end = int(input("Muestra final: "))
            vowel = input("Vocal: ") 
            if vowel in VOWELS:
                gen_db(data[start:end], vowel)
                
            else:
                print("Vocal incorrecta!")
                show_options(data)
        except Exception as e:
            print("Error en las muestra inicial o final: ", e)
            show_options(data)
    elif x =="3":
        sys.exit()
    else:
        print("Opcion incorrecta!")
        show_options(data)

for file in unprocessed_files:
    print("Archivo actual: ", file)
    fs, data = wavfile.read(file)
    assert(fs == 8000)
    show_options(data)
    
        
