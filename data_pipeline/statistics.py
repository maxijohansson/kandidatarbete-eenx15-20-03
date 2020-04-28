import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.join(os.path.dirname( __file__ ), '..')


data_path = BASE_DIR + '\\data\\phase_3\\avg_envelope_n10\\'

ds_factor = 10
locs = ['fotbollsplan', 'maskinhuset', 'ronnvagen', 'SB', 'sven_hultin', 'zaloonen']
datasets = {}

for loc in locs:
	datasets[loc] = pd.read_csv(data_path + '{}.csv'.format(loc), index_col=0)

df = pd.concat([datasets[loc] for loc in locs])
df = df.sample(frac=1).reset_index(drop=True)
X = df.iloc[:,:-1]
y = df.iloc[:,-1]
X = X.iloc[:, ds_factor-1::ds_factor]
df = pd.concat([X,y], axis='columns')

data = df.iloc[:,:-1].values.T
dry = df[df['label'] == 'dry'].iloc[:,:-1].values.T
wet = df[df['label'] == 'wet'].iloc[:,:-1].values.T
# dry = df.iloc[:1000,:-1].values.T
# wet = df.iloc[1000:2000,:-1].values.T

avg_dry = np.mean(dry, axis=1)
avg_wet = np.mean(wet, axis=1)

cov_dry = np.cov(dry)
cov_wet = np.cov(wet)

distance = np.linalg.norm(avg_wet-avg_dry)

avg_s_dry = np.mean(np.sqrt(np.diag(cov_dry)))
avg_s_wet = np.mean(np.sqrt(np.diag(cov_wet)))

print(distance)
print(avg_s_dry)
print(avg_s_wet)