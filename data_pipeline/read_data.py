import os
import numpy as np
import h5py
import matplotlib.pyplot as plt
from matplotlib.path import Path
import plotly.graph_objects as go

BASE_DIR = os.path.join(os.path.dirname( __file__ ), '..')


data_path = '\\data\\matning1.h5'
f = h5py.File(BASE_DIR + data_path, 'r')

print(f.keys())
print(f['data'])
dset = f['data']

print(dset.shape)

i = dset[:,0,:]
i_avg = np.average(i, axis=0)

q = dset[:,1,:]
q_avg = np.average(q, axis=0)

print(i.shape)
print(q.shape)

Ir_avg = [x.real for x in i_avg]
Ii_avg = [x.imag for x in i_avg]

Qr_avg = [x.real for x in q_avg]
Qi_avg = [x.imag for x in q_avg]

fig = go.Figure(
	data = [
		go.Scatter(
			x = Ir_avg, 
			y = Ii_avg, 
			line = dict(
				color = 'blue',
				width = 5
			)
		),
		go.Scatter(
			x = Qr_avg, 
			y = Qi_avg,
			line = dict(
				color = 'red',
				width = 5
			)
		)
	]
)

for j in range(20):
	Ir = [x.real for x in i[j]]
	Ii = [x.imag for x in i[j]]

	Qr = [x.real for x in q[j]]
	Qi = [x.imag for x in q[j]]

	fig.add_trace(go.Scatter(		
		x = Ir, 
		y = Ii, 
		line = dict(
			color = 'blue',
			dash = 'dot',
			width = 0.3)
		)
	)
	fig.add_trace(go.Scatter(		
		x = Qr, 
		y = Qi, 
		line = dict(
			color = 'red',
			dash = 'dot',
			width = 0.3)
		)
	)


# fig.show()

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
