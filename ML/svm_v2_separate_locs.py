import os
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn import svm

BASE_DIR = os.path.join(os.path.dirname( __file__ ), '..')


data_path = BASE_DIR + '\\data\\phase_2\\'

df_mg = pd.read_csv(data_path + 'envelope_maskingrand_25avg.csv', index_col=0)

df_mh = pd.read_csv(data_path + 'envelope_maskinhuset_25avg.csv', index_col=0)

df_za = pd.read_csv(data_path + 'envelope_zaloonen_25avg.csv', index_col=0)

print('Length of datasets:')
print('df_mg: ' + str(len(df_mg.index)))
print('df_mh: ' + str(len(df_mh.index)))
print('df_za: ' + str(len(df_za.index)))

train = pd.concat([df_mg, df_mh])
test = df_za

train_dry = train[train['label'] == 'dry']	# To get the same amount of training data for each label
train_dry = train_dry.iloc[:340, :]
train_wet = train[train['label'] == 'wet']
train_wet = train_wet.iloc[:340, :]
train = pd.concat([train_dry, train_wet])

train = train.sample(frac=1).reset_index(drop=True)
test = test.sample(frac=1).reset_index(drop=True)

X_train = train.iloc[:, :-1]
X_test = test.iloc[:, :-1]
y_train = train.iloc[:,-1]
y_test = test.iloc[:,-1]
print(y_test)

clf = svm.SVC(gamma='scale')

clf.fit(X_train, y_train)

for i in range(20):
    print(clf.predict([X_test.iloc[i,0:]]), y_test[i])

print('Accuracy:')
print(clf.score(X_test, y_test))
