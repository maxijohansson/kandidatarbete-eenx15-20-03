import os
import pandas as pd
import numpy as np  
import h5py
import json
import matplotlib.pyplot as plt
import plotly.graph_objects as go

import data_utils as utils

BASE_DIR = os.path.join(os.path.dirname( __file__ ), '..')

n = 10
data_path = BASE_DIR + '\\data\\phase_2\\dry\\'

files = os.listdir(data_path)

dry = pd.DataFrame()

for file in files:
	df = utils.read_data(data_path + file)
	df = utils.amplitude(df)

	dry = pd.concat([dry, df])

dry = dry.rolling(n).mean() 
dry = dry.iloc[::n, :]

dry.dropna(inplace=True)

dry['label'] = 'dry'

data_path = BASE_DIR + '\\data\\phase_2\\wet\\'

files = os.listdir(data_path)

wet = pd.DataFrame()

for file in files:
	df = utils.read_data(data_path + file)
	df = utils.amplitude(df)


	wet = pd.concat([wet, df])

wet = wet.rolling(n).mean() 
wet = wet.iloc[::n, :]

wet.dropna(inplace=True)

wet['label'] = 'wet'


features = pd.concat([dry, wet])
features.reset_index(inplace=True, drop=True)

print(features)
features.to_csv(BASE_DIR + '\\data\\phase_2\\envelope_10avg.csv')