import os
import pandas as pd
import numpy as np  

import data_utils as utils

BASE_DIR = os.path.join(os.path.dirname( __file__ ), '..')

files = []

files.append('\\data\\avg_envs\\phase_2_wet')

for file in files[:1]:
	df = pd.read_csv(BASE_DIR + file, index_col=0)

print(df)