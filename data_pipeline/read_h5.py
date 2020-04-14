import os
import pandas as pd
import numpy as np  
import h5py
import json

import data_utils as utils

BASE_DIR = os.path.join(os.path.dirname( __file__ ), '..')

# path = BASE_DIR + '\\data\\phase_2\\maskingrand_move_30_3.h5'
# f = h5py.File(path, 'r')

# print(f.keys())
# print(f['data'])

data_path = BASE_DIR + '\\data\\phase_2\\dry'

files = os.listdir(data_path)
for file in files:
	print(file)