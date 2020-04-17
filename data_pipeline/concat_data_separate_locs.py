import os
import pandas as pd
import numpy as np  
import h5py
import json
import matplotlib.pyplot as plt
import plotly.graph_objects as go

import data_utils as utils

BASE_DIR = os.path.join(os.path.dirname( __file__ ), '..')

n = 25
data_path = BASE_DIR + '\\data\\phase_2\\dry\\'

files = os.listdir(data_path)

dry_mh = pd.DataFrame()
dry_mg = pd.DataFrame()
dry_za = pd.DataFrame()

for file in files:
	df = utils.read_data(data_path + file)
	df = utils.amplitude(df)

	if 'maskingrand' in file:	
		dry_mg = pd.concat([dry_mg, df])
	elif 'maskinhuset' in file:
		dry_mh = pd.concat([dry_mh, df])
	elif 'zaloonen' in file:
		dry_za = pd.concat([dry_za, df])

print('Length of datasets:')
print('df_mg: ' + str(len(dry_mg.index)))
print('df_mh: ' + str(len(dry_mh.index)))
print('df_za: ' + str(len(dry_za.index)))

dry_mg = dry_mg.rolling(n).mean() 
dry_mg = dry_mg.iloc[24::n, :]
dry_mh = dry_mh.rolling(n).mean() 
dry_mh = dry_mh.iloc[24::n, :]
dry_za = dry_za.rolling(n).mean() 
dry_za = dry_za.iloc[24::n, :]

dry_mg.dropna(inplace=True)
dry_mh.dropna(inplace=True)
dry_za.dropna(inplace=True)

dry_mg.loc[:,'label'] = 'dry'
dry_mh.loc[:,'label'] = 'dry'
dry_za.loc[:,'label'] = 'dry'

data_path = BASE_DIR + '\\data\\phase_2\\wet\\'

files = os.listdir(data_path)

wet_mh = pd.DataFrame()
wet_mg = pd.DataFrame()
wet_za = pd.DataFrame()

for file in files:
	df = utils.read_data(data_path + file)
	df = utils.amplitude(df)

	if 'maskingrand' in file:	
		wet_mg = pd.concat([wet_mg, df])
	elif 'maskinhuset'in file:
		wet_mh = pd.concat([wet_mh, df])
	elif 'zaloonen' in file:
		wet_za = pd.concat([wet_za, df])

wet_mg = wet_mg.rolling(n).mean() 
wet_mg = wet_mg.iloc[24::n, :]
wet_mh = wet_mh.rolling(n).mean() 
wet_mh = wet_mh.iloc[24::n, :]
wet_za = wet_za.rolling(n).mean() 
wet_za = wet_za.iloc[24::n, :]

wet_mg.dropna(inplace=True)
wet_mh.dropna(inplace=True)
wet_za.dropna(inplace=True)

wet_mg.loc[:,'label'] = 'wet'
wet_mh.loc[:,'label'] = 'wet'
wet_za.loc[:,'label'] = 'wet'

features_mg = pd.concat([dry_mg, wet_mg])
features_mh = pd.concat([dry_mh, wet_mh])
features_za = pd.concat([dry_za, wet_za])
features_mg.reset_index(inplace=True, drop=True)
features_mh.reset_index(inplace=True, drop=True)
features_za.reset_index(inplace=True, drop=True)

print(len(features_mh.index))
features_mg.to_csv(BASE_DIR + '\\data\\phase_2\\envelope_maskingrand_25avg.csv')
features_mh.to_csv(BASE_DIR + '\\data\\phase_2\\envelope_maskinhuset_25avg.csv')
features_za.to_csv(BASE_DIR + '\\data\\phase_2\\envelope_zaloonen_25avg.csv')