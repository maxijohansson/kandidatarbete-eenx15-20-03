import sklearn
import numpy as np
from sklearn import svm

f = open("../../kandidatarbete-eenx15-20-03/data/phase_2/envelope_25avg.csv")
f.readline()
data = np.loadtxt(f, dtype=str, delimiter=',') 

data = data[1:,1:] #Skär bort översta raden och första kolumnen
data = data[38:,:] #För att ha lika många datapunkter som dry och wet
np.random.shuffle(data) #Blandar raderna så att eventuella bias försvinner om hur modellen tränas

nr_tests = 100
X = data[:-nr_tests,1:-1]
X = X.astype(np.float)


test = data[-nr_tests:,1:-1]
test = test.astype(np.float)
#print(test[-1,1:])

Y = data[:-nr_tests,-1]
test_labels = data[-nr_tests:,-1]
print(X.shape, test.shape)

#clf = svm.NuSVC(gamma='auto')# Denna classifiern ger endast "dry"
clf = svm.SVC() # Denna är king!
clf.fit(X, Y)

"""
test_pos = 0
print("Predicted: ", clf.predict(test[test_pos, 0:].reshape(1,-1)))
print( "Actual: ", test_labels[test_pos])

"""
Y_est = np.empty([nr_tests, 1], dtype=str)
for i in range(nr_tests):
    #np.append(Y_est, clf.predict(test[i, 0:].reshape(1,-1)))
    print(clf.predict(test[i, 0:].reshape(1,-1)), test_labels[i])
    
print("Accuracy: ", clf.score(test, test_labels))
