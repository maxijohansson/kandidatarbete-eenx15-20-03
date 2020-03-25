import os
import pandas as pd
import numpy as np  
import h5py
import json

BASE_DIR = os.path.join(os.path.dirname( __file__ ), '..')


path = BASE_DIR + '\\data\\nollmatning\\scania_0324_30_1.h5'
# def read_data(path):
f = h5py.File(path, 'r')

print(f.keys())
