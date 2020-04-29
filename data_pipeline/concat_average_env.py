import os
import pandas as pd
import numpy as np  
import h5py
import json
import matplotlib.pyplot as plt
import plotly.graph_objects as go


import data_utils as utils

BASE_DIR = os.path.join(os.path.dirname( __file__ ), '..')


data_path = BASE_DIR + '\\data\\phase_3\\raw_data\\wet\\'

files = os.listdir(data_path)

amplitudes = pd.DataFrame()
x = []
i = 0

for file in files:
	# if 'raf' not in file:
	# print(file)
	_df = utils.read_data(data_path + file)
	_df = utils.amplitude(_df)
	if i == 0:
		meta = utils.read_meta(data_path + file)
		d = meta['step_length_m']
		x = [meta['range_start_m'] + d*i for i in range(meta['data_length'])]
		i = 1

	amplitudes = pd.concat([amplitudes, _df])

print(amplitudes.shape)
amplitudes.dropna(inplace=True)
avg_amplitudes = amplitudes.mean(axis='rows')
std_up = avg_amplitudes + amplitudes.std()
std_dn = avg_amplitudes - amplitudes.std()

df = pd.DataFrame([x, avg_amplitudes, std_up, std_dn])


print(df)
df.to_csv(BASE_DIR + '\\data\\avg_envs\\phase_3_wet.csv')