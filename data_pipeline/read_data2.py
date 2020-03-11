import os
import pandas as pd
import numpy as np  
import h5py

import plotly.graph_objects as go


BASE_DIR = os.path.join(os.path.dirname( __file__ ), '..')


# input: 	string path to h5 file
# output: 	pandas dataframe with frames as rows and depth samples as columns
def read_data(path):
	f = h5py.File(path, 'r')
	data = np.squeeze(f['data'][:,:,:])
	index = [i for i in range(data.shape[0])]

	return pd.DataFrame(data=data, index=index)


# input:	pandas dataframe with columns of iq data in complex numbers
# output:	two pandas dataframea with columns for each depth sample's amplitude and phase
def polar(input):
	amplitude = pd.DataFrame()
	phase = pd.DataFrame()
	columns = input.columns
	for column in columns:
		amplitude['%s' % column] = input[column].apply(np.absolute)
		phase['%s' % column] = input[column].apply(np.angle)

	return amplitude, phase


iq = read_data(BASE_DIR + '\\data\\phase_1\\asfalt1.h5')
amplitude, phase = polar(iq)


trace1 = go.Scatter(
			x = [i for i in amplitude.columns], 
			y = amplitude.mean(axis='rows'), 
			line = dict(
				color = 'blue',
				width = 2
			)
		)

trace2 = go.Scatter(
			x = [i for i in amplitude.columns], 
			y = phase.mean(axis='rows'),
			line = dict(
				color = 'red',
				width = 2
			),
			yaxis = 'y2'
		)

data = [trace1, trace2]

layout = go.Layout(
    yaxis = dict(
        title = 'amplitude'
    ),
    yaxis2 = dict(
        title = 'phase',
        titlefont = dict(
            color='rgb(148, 103, 189)'
        ),
        tickfont=dict(
            color='rgb(148, 103, 189)'
        ),
        overlaying='y',
        side='right'
    )
)

fig = go.Figure(
	data = data,
	layout = layout
)

fig.show()