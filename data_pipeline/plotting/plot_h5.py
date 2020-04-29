import os
import pandas as pd
import numpy as np  
import h5py
import json
import matplotlib.pyplot as plt
import plotly.graph_objects as go

import data_utils as utils

BASE_DIR = os.path.join(os.path.dirname( __file__ ), '..\\..')

files = []

# files.append('\\data\\nollmatning\\nollmatning_hallplats3.h5')
# files.append('\\data\\nollmatning\\nollmatning_vid_fotbollsplan.h5')
# files.append('\\data\\nollmatning\\nollmatning_hallplats.h5')
# files.append('\\data\\nollmatning\\nollmatning_hallplats.h5')

# files.append('\\data\\phase_2\\wet\\maskinhuset_move_wet_30_2.h5')
# files.append('\\data\\phase_2\\dry\\maskinhuset_move_30_14.h5')

# files.append('\\data\\phase_3\\raw_data\\dry\\ronnvagen_dry_2.h5')
files.append('\\data\\phase_3\\raw_data\\wet\\ronnvagen_wet_2.h5')

# # files.append('\\data\\phase_4\\skidome_1.h5')
# files.append('\\data\\phase_4\\skidome_20.h5')
# files.append('\\data\\phase_4\\skidome_raf_1.h5')
# files.append('\\data\\phase_4\\skidome_raf_32.h5')

# files.append('\\data\\phase_5\\ronnvagen_dry_2_ra0.h5')
files.append('\\data\\phase_5\\wet\\ronnvagen_wet_2_ra0.h5')


ys = []
xs = []
names = []
colors = ['#0074D9', '#FF4136', '#3D9970', '#FF851B', '#B10DC9', '#AAAAAA', '#001f3f', '#7FDBFF']

for i,file in enumerate(files):
	df = utils.read_data(BASE_DIR + file)
	meta = utils.read_meta(BASE_DIR + file)
	amplitude, phase = utils.polar(df)
	names.append(file)
	# amplitude = df

	d = meta['step_length_m']
	x = [meta['range_start_m'] + d*i for i in range(meta['data_length'])]
	xs.append(x)

	ys.append([])
	ys[i].append(amplitude.mean(axis='rows'))
	ys[i].append(ys[i][0] + amplitude.std())
	ys[i].append(ys[i][0] - amplitude.std())

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