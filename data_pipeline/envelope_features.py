import os
import pandas as pd
import numpy as np  
import h5py
import json
import matplotlib.pyplot as plt
import plotly.graph_objects as go


import data_utils as utils

BASE_DIR = os.path.join(os.path.dirname( __file__ ), '..')


data_path = BASE_DIR + '\\data\\phase_3\\raw_data\\dry\\'

files = os.listdir(data_path)

dry = pd.DataFrame()

for file in files:
	df = utils.read_data(data_path + file)
	df = utils.amplitude(df)
	n = 25
	df = df.rolling(n).mean() 
	df = df.iloc[::n, :]

	dry = pd.concat([dry, df])

dry.dropna(inplace=True)

dry['label'] = 'dry'

data_path = BASE_DIR + '\\data\\phase_3\\raw_data\\wet\\'

files = os.listdir(data_path)

wet = pd.DataFrame()

for file in files:
	df = utils.read_data(data_path + file)
	df = utils.amplitude(df)
	n = 25
	df = df.rolling(n).mean() 
	df = df.iloc[::n, :]

	wet = pd.concat([wet, df])

wet.dropna(inplace=True)

wet['label'] = 'wet'


features = pd.concat([dry, wet])
features.reset_index(inplace=True, drop=True)

print(features)
features.to_csv(BASE_DIR + '\\data\\avg_envs\\phase_')