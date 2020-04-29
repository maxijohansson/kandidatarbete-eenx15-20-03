import os
import pandas as pd
import numpy as np  
import h5py
import json
import matplotlib.pyplot as plt
import plotly.graph_objects as go

import data_utils as utils

BASE_DIR = os.path.join(os.path.dirname( __file__ ), '..')

files = []

# files.append('\\data\\avg_envs\\phase_2_dry.csv')
# files.append('\\data\\avg_envs\\phase_2_wet.csv')

# files.append('\\data\\avg_envs\\phase_3_dry.csv')
# files.append('\\data\\avg_envs\\phase_3_wet.csv')

files.append('\\data\\avg_envs\\phase_4_snow_ra0.csv')
files.append('\\data\\avg_envs\\phase_4_snow_ra7.csv')

ys = []
xs = []
names = []
colors = ['#0074D9', '#FF4136', '#3D9970', '#FF851B', '#B10DC9', '#AAAAAA', '#001f3f', '#7FDBFF']

for i,file in enumerate(files):
    df = pd.read_csv(BASE_DIR + file, index_col=0)
    names.append(file)
    xs.append(df.iloc[0,:])
    ys.append([])
    ys[i].append(df.iloc[1,:])
    ys[i].append(df.iloc[2,:])
    ys[i].append(df.iloc[3,:])

data = []
j = 0
for x,y in zip(xs,ys):
    opacities = [1.0, 0.25, 0.25]
    for i,y in enumerate(y):
        data.append(
            dict(
            x = x,
            y = y,
            opacity = opacities[i],
            mode = 'markers',
            name = names[j],
            marker = {
                'size': 2,
                'color': colors[j],
            })
        )
    j = j+1

fig = go.Figure({
    'data': data,
    'layout': dict(
        xaxis = {
            'title': 'distance (m)',
            'tickmode': 'linear',
            'dtick': 0.05,
        },
        yaxis = {
            'title': 'amplitude',
        },
        margin = {'l': 50, 'b': 30, 't': 10, 'r': 0},
        hovermode = 'closest',
        showlegend=True,
        legend= {'itemsizing': 'constant'}
    )
 })

fig.show()

# plt.plot(x, drys, color='blue')
# plt.plot(x, drys + drys.std(), color='blue', linestyle='dashed')
# plt.plot(x, drys - drys.std(), color='blue', linestyle='dashed')

# plt.plot(x, wets, color='red')
# plt.plot(x, wets + wets.std(), color='red', linestyle='dashed')
# plt.plot(x, wets - wets.std(), color='red', linestyle='dashed')
# # plt.plot(x, wet.mean(axis='rows'))
# plt.show()