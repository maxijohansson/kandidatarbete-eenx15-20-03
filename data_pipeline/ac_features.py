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
locs = ['fotbollsplan', 'maskinhuset', 'ronnvagen', 'SB', 'sven_hultin', 'zaloonen']

label = 'dry'
drys = {loc: pd.DataFrame() for loc in locs}

data_path = BASE_DIR + '\\data\\phase_3\\ac_features\\ds16_q5_T50\\separate\\{}\\'.format(label)
files = os.listdir(data_path)

for file in files:
	df = pd.read_csv(data_path + file, header=None)

	for loc in locs:
		if loc in file:
			drys[loc] = pd.concat([drys[loc], df])

for loc in locs:
	# drys[loc] = drys[loc].rolling(n).mean()
	# drys[loc] = drys[loc].iloc[n-1::n, :]

	drys[loc].dropna(inplace=True)

	drys[loc].loc[:,'label'] = label
	print('dry {}: {}'.format(loc, len(drys[loc])))

label = 'wet'
wets = {loc: pd.DataFrame() for loc in locs}

data_path = BASE_DIR + '\\data\\phase_3\\ac_features\\ds16_q5_T50\\separate\\{}\\'.format(label)
files = os.listdir(data_path)

for file in files:
	df = pd.read_csv(data_path + file, header=None)

	for loc in locs:
		if loc in file:
			wets[loc] = pd.concat([wets[loc], df])

for loc in locs:
	# wets[loc] = wets[loc].rolling(n).mean()
	# wets[loc] = wets[loc].iloc[n-1::n, :]

	wets[loc].dropna(inplace=True)

	wets[loc].loc[:,'label'] = label
	print('wet {}: {}'.format(loc, len(wets[loc])))

# features = {loc: pd.DataFrame() for loc in locs}
for loc in locs:
	df = pd.concat([drys[loc], wets[loc]])
	df.reset_index(inplace=True, drop=True)
	print(loc + ': ' + str(len(df)))

	save_path = BASE_DIR + '\\data\\phase_3\\ac_features\\ds16_q5_T50'.format(n)
	try:
		os.mkdir(save_path)
	except OSError:
	    print ('Create folder failed')
	else:
	    print ('Successfully created folder')
	df.to_csv('{}\\{}.csv'.format(save_path, loc))