import os
import pandas as pd
import numpy as np  
import h5py
import json

BASE_DIR = os.path.join(os.path.dirname( __file__ ), '..')


path = BASE_DIR + '\\data\\phase_1\\asfalt1.h5'
# def read_data(path):
f = h5py.File(path, 'r+')
# with h5py.File(path, 'r+') as f:
# 	f['data_info'] = 'asfalt parkering'
data = np.squeeze(f['data'][:,:,:])
# index = [i for i in range(data.shape[0])]


print(f.keys())
meta = json.loads(str(f['session_info'][...]))
meta2 = json.loads(str(f['sensor_config_dump'][...]))
meta.update(meta2)

print(meta)
