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

	amplitude = input.apply(np.absolute)
	phase = input.apply(np.angle)

	return amplitude, phase


def make_2d_trace(x, y, width=2, color='blue', dash='solid', yaxis='y1', name='trace'):
	trace = go.Scatter(
			x = x,
			y = y,
			line = dict(
				color = color,
				width = width,
				dash = dash
			),
			yaxis = yaxis,
			name = name
		)

	return trace


# input:	pandas dataframe with iq data
# plots amplitude and phase
def plot_amplitude_phase(iqs, dparams, title = ''):
	
	layout = go.Layout(
		xaxis = dict(
			title = 'distance (cm)'
			),
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
	    ),
	    title = title
	)

	fig = go.Figure(
		layout = layout
	)

	colors = ['blue', 'red', 'green', 'orange']

	for n,iq in enumerate(iqs):
		print('Adding traces file ' + str(n+1) + '...')

		amplitude, phase = polar(iq)
		print('   Extracted amplitude and phase')
		
		d = (dparams[1]-dparams[0])/(len(amplitude.columns)-1)
		x =  [dparams[0] + i*d for i in range(len(amplitude.columns))]
		trace1 = make_2d_trace(x, amplitude.mean(axis='rows'), color=colors[n], name='amplitude')
		trace2 = make_2d_trace(x, phase.mean(axis='rows'), color=colors[n], dash='dash', yaxis='y2', name='phase')
		print('   Constructed traces')

		fig.add_trace(trace1)
		fig.add_trace(trace2)

		# for row in phase.loc[0:10, :].index:
		# 	t = make_2d_trace(phase.loc[row], width=0.3)
		# 	fig.add_trace(t)

	print('Plotting!')
	fig.show()


def plot_iq(iqs):
	fig = go.Figure()
	colors = ['blue', 'red', 'green', 'orange']

	for n,iq in enumerate(iqs):
		iq_avg = iq.mean(axis='rows')
		i = [x.real for x in iq_avg]
		q = [x.imag for x in iq_avg]

		fig.add_trace(go.Scatter(		
			x = i, 
			y = q, 
			line = dict(
				color = colors[n],
				dash = 'solid',
				width = 1)
			)
		)

	fig.show()


if __name__ == '__main__':

	print('Starting...')
	iqs = []

	iqs.append(read_data(BASE_DIR + '\\data\\nollmatning\\nollmatning_hallplats3.h5'))
	# iqs.append(read_data(BASE_DIR + '\\data\\nollmatning\\nollmatning_hallplats4.h5'))
	# iqs.append(read_data(BASE_DIR + '\\data\\nollmatning\\nollmatning_hallplats3.h5'))

	# iqs.append(read_data(BASE_DIR + '\\data\\phase_1\\asfalt\\parkering_zaloonen_0318_3.h5'))
	iqs.append(read_data(BASE_DIR + '\\data\\phase_1\\asfalt\\parkering_zaloonen_0318_1.h5'))
	# iqs.append(read_data(BASE_DIR + '\\data\\phase_1\\asfalt\\gibraltar_0318_1.h5'))
	# iqs.append(read_data(BASE_DIR + '\\data\\phase_1\\asfalt\\gibraltar_0318_2.h5'))

	# iqs.append(read_data(BASE_DIR + '\\data\\phase_1\\metal1.h5'))
	# iqs.append(read_data(BASE_DIR + '\\data\\phase_1\\wet2.h5'))

	dparams = [15, 200]
	print('Plotting curves...')
	plot_amplitude_phase(iqs, dparams, title='Asfalt vs metall (röd)')
	# plot_iq(iqs)
