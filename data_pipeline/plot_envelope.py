import os
import pandas as pd
import numpy as np  
import h5py
import json
import matplotlib.pyplot as plt
import plotly.graph_objects as go

import data_utils as utils

BASE_DIR = os.path.join(os.path.dirname( __file__ ), '..')


data_path = BASE_DIR + '\\data\\phase_2\\dry\\'

files = os.listdir(data_path)
n = 10

dry = pd.DataFrame()

for file in files:
	
	df = utils.read_data(data_path + file)
	df = utils.amplitude(df)
	df = df.rolling(n).mean() 
	df = df.iloc[::n, :]

	dry = pd.concat([dry, df])

dry.dropna(inplace=True)

dry['label'] = 'dry'
# print(dry)


data_path = BASE_DIR + '\\data\\phase_2\\wet\\'

files = os.listdir(data_path)

wet = pd.DataFrame()

for file in files:
	df = utils.read_data(data_path + file)
	df = utils.amplitude(df)
	df = df.rolling(n).mean() 
	df = df.iloc[::n, :]

	wet = pd.concat([wet, df])

wet.dropna(inplace=True)

wet['label'] = 'wet'
# print(wet)

x = wet.columns[:-1]
drys = dry.mean(axis='rows')
wets = wet.mean(axis='rows')

fig = go.Figure()

fig.add_trace(go.Scatter(
	x = x, 
	y = drys,
	name = 'dry',
	line = dict(
		color = 'blue'
	)
))
fig.add_trace(go.Scatter(
	x = x, 
	y = drys + drys.std(),
	name = 'dry',
	line = dict(
		color = 'blue',
		dash = 'dash'
	)
))
fig.add_trace(go.Scatter(
	x = x, 
	y = drys - drys.std(),
	name = 'dry',
	line = dict(
		color = 'blue',
		dash = 'dash'
	)
))

fig.add_trace(go.Scatter(
	x = x, 
	y = wets,
	name = 'wet',
	line = dict(
		color = 'red'
	)
))
fig.add_trace(go.Scatter(
	x = x, 
	y = wets + wets.std(),
	name = 'wet',
	line = dict(
		color = 'red',
		dash = 'dash'
	)
))
fig.add_trace(go.Scatter(
	x = x, 
	y = wets - wets.std(),
	name = 'wet',
	line = dict(
		color = 'red',
		dash = 'dash'
	)
))

fig.update_layout(
	title = 'Average envelope shape of sweeps on dry and wet asfalt',
	xaxis_title = 'feature',
	yaxis_title = 'amplitude'
)

fig.show()

# plt.plot(x, drys, color='blue')
# plt.plot(x, drys + drys.std(), color='blue', linestyle='dashed')
# plt.plot(x, drys - drys.std(), color='blue', linestyle='dashed')

# plt.plot(x, wets, color='red')
# plt.plot(x, wets + wets.std(), color='red', linestyle='dashed')
# plt.plot(x, wets - wets.std(), color='red', linestyle='dashed')
# # plt.plot(x, wet.mean(axis='rows'))
# plt.show()