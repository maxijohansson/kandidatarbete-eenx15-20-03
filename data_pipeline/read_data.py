import os
import numpy as np
import h5py
import matplotlib.pyplot as plt
from matplotlib.path import Path
import plotly.graph_objects as go

BASE_DIR = os.path.join(os.path.dirname( __file__ ), '..')


def read_data_from_h5(path):
	f = h5py.File(path, 'r')
	return f['data']


data_path = '\\data\\phase_1\\asfalt1.h5'
# data_path = '\\data\\nollmatning\\nollmatning_hallplats.h5'

f = h5py.File(BASE_DIR + data_path, 'r')

print(f.keys())
print(f['data'])
sample1 = f['data']

data_path = '\\data\\phase_1\\asfalt2.h5'
# data_path = '\\data\\nollmatning\\nollmatning_.h5'

f = h5py.File(BASE_DIR + data_path, 'r')

print(f.keys())
print(f['data'])
sample2 = f['data']

sample1 = sample1[:,0,:]
sample1_avg = np.average(sample1, axis=0)

sample2 = sample2[:,0,:]
sample2_avg = np.average(sample2, axis=0)


sample1_real = [x.real for x in sample1_avg]
sample1_imag = [x.imag for x in sample1_avg]
x = [i for i in range(len(sample1))]
sample1_phase = np.arctan([q/i for q, i in zip(sample1_real, sample1_imag)])

sample2_real = [x.real for x in sample2_avg]
sample2_imag = [x.imag for x in sample2_avg]

fig = go.Figure(
	data = [
		go.Scatter(
			x = x, 
			y = sample1_phase, 
			line = dict(
				color = 'blue',
				width = 5
			)
		),
		# go.Scatter(
		# 	x = sample2_real, 
		# 	y = sample2_imag,
		# 	line = dict(
		# 		color = 'red',
		# 		width = 5
		# 	)
		# )
	]
)

# for j in range(20):
# 	sample1_real = [x.real for x in sample1[j]]
# 	sample1_imag = [x.imag for x in sample1[j]]

# 	sample2_real = [x.real for x in sample2[j]]
# 	sample2_imag = [x.imag for x in sample2[j]]

# 	fig.add_trace(go.Scatter(		
# 		x = sample1_real, 
# 		y = sample1_imag, 
# 		line = dict(
# 			color = 'blue',
# 			dash = 'dot',
# 			width = 0.3)
# 		)
# 	)
	# fig.add_trace(go.Scatter(		
	# 	x = sample2_real, 
	# 	y = sample2_imag, 
	# 	line = dict(
	# 		color = 'red',
	# 		dash = 'dot',
	# 		width = 0.3)
	# 	)
	# )


fig.show()

# for i in range(5):

# 	subset1 = dset[i][0]
# 	subset2 = dset[i][1]


# 	X2 = [x.real for x in subset2]
# 	Y2 = [y.imag for y in subset2]

# 	# plt.plot(X1,Y1, color='red')
# 	# plt.plot(X2,Y2, color='blue')
# 	# plt.show()


# 	fig = go.Figure(
# 		data=[go.Scatter(x=X1, y=Y1), go.Scatter(x=X2, y=Y2)]
# 		)
# 	fig.show()
