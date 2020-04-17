import os
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn import svm

BASE_DIR = os.path.join(os.path.dirname( __file__ ), '..')


data_path = BASE_DIR + '\\data\\phase_2\\'

datasets = {}

datasets['maskingrand'] = pd.read_csv(data_path + 'envelope_maskingrand_25avg.csv', index_col=0)
datasets['maskinhuset'] = pd.read_csv(data_path + 'envelope_maskinhuset_25avg.csv', index_col=0)
datasets['zaloonen'] = pd.read_csv(data_path + 'envelope_zaloonen_25avg.csv', index_col=0)

print('Size of datasets:')
for key in datasets.keys():
	print(key + ': ' + str(len(datasets[key].index)))

for key, dataset in datasets.items():
	train_keys = [k for k in datasets.keys() if k not in [key]]
	train_sets = [datasets[train_key] for train_key in train_keys]
	train = pd.concat(train_sets)
	test = dataset

	train_size = min([len(train_set) for train_set in train_sets]) * 2		# The optimal size of each train set

	train_dry = train[train['label'] == 'dry']			# To get the same amount of training data for each label
	train_dry = train_dry.iloc[:int(train_size/2), :]
	train_wet = train[train['label'] == 'wet']
	train_wet = train_wet.iloc[:int(train_size/2), :]
	train = pd.concat([train_dry, train_wet])

	train = train.sample(frac=1).reset_index(drop=True)		# Shuffle
	test = test.sample(frac=1).reset_index(drop=True)

	X_train = train.iloc[:, :-1]
	X_test = test.iloc[:, :-1]
	y_train = train.iloc[:,-1]
	y_test = test.iloc[:,-1]

	clf = svm.SVC(gamma='scale')

	clf.fit(X_train, y_train)

	# for i in range(20):
	#     print(clf.predict([X_test.iloc[i,0:]]), y_test[i])
	print()
	print(key + ' as test set: ')
	print('Train size: ' + str(train_size))
	print('Accuracy: ' + str(clf.score(X_test, y_test)))
