import os
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = os.path.join(os.path.dirname( __file__ ), '..')


data_path = BASE_DIR + '\\data\\phase_2'
df = pd.read_csv(data_path + '\\wet_dry_envelope_unprocessed.csv', index_col=0)


dry_mean = df[df['label'] == 'dry'].mean(axis='rows')
wet_mean = df[df['label'] == 'wet'].mean(axis='rows')

# print(dry_mean)
x = df.columns[:-1]
plt.plot(x, dry_mean)
plt.plot(x, wet_mean)


plt.show()
