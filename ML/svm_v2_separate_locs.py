import os
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import balanced_accuracy_score


BASE_DIR = os.path.join(os.path.dirname( __file__ ), '..')


data_path = BASE_DIR + '\\data\\phase_3\\avg_envelope_n10\\'

datasets = {}
ds_factor = 300
locs = ['fotbollsplan', 'maskinhuset', 'ronnvagen', 'SB', 'sven_hultin', 'zaloonen']

for loc in locs:
	_df = pd.read_csv(data_path + '{}.csv'.format(loc), index_col=0)
	X = _df.iloc[:,:-1]
	y = _df.iloc[:,-1]
	X = X.iloc[:, ds_factor-1::ds_factor]
	datasets[loc] = pd.concat([X,y], axis=1)

print('Size of datasets:')
for key in datasets.keys():
	print(key + ': ' + str(datasets[key].shape))
print()

for key, dataset in datasets.items():
	print('-----------------------------------------')
	print(key + ' as test set')
	train_keys = [k for k in datasets.keys() if k not in [key]]

	train_sets = [datasets[train_key] for train_key in train_keys]
	train = pd.concat(train_sets)
	print()
	test = dataset

	train_size = min([len(train_set) for train_set in train_sets]) * len(train_keys)		# The optimal size of each train set

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

	clf = SVC(kernel='rbf', gamma='scale')
	# clf = LinearSVC()
	# clf = SGDClassifier(loss="hinge", penalty="l2", max_iter=5)
	# clf = RandomForestClassifier(n_estimators=10)
	# clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
	# clf = KNeighborsClassifier(n_neighbors=15)

	print('Train size: ' + str(train_size))
	print('Training model...')
	clf.fit(X_train, y_train)

	# for i in range(20):
	#     print(clf.predict([X_test.iloc[i,0:]]), y_test[i])

	print('Accuracy: ' + str(clf.score(X_test, y_test)))
	print()


print('-----------------------------------------')
print('Random test set')

df = pd.concat([datasets[loc] for loc in locs])
X = df.iloc[:,:-1]
y = df.iloc[:,-1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

clf = SVC(kernel='rbf', gamma='scale')
# clf = LinearSVC()
# clf = SGDClassifier(loss="hinge", penalty="l2", max_iter=5)
# clf = RandomForestClassifier(n_estimators=10)
# clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
# clf = KNeighborsClassifier(n_neighbors=15)

print('Train size: ' + str(len(X_train.index)))
print('Training model...')
clf.fit(X_train, y_train)

# for i in range(20):
#     print(clf.predict([X_test.iloc[i,0:]]), y_test[i])

print('Accuracy: ' + str(clf.score(X_test, y_test)))
print()
