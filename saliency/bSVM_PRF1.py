import sys
import math
import pickle
import random
import numpy as np
from sklearn import svm

f=open("/Users/yalunzheng/Documents/BioPre/saliency/local/trainlist.pkl","rb")
train_list=pickle.load(f)
f.close()

f=open("/Users/yalunzheng/Documents/BioPre/saliency/local/testlist.pkl","rb")
test_list=pickle.load(f)
f.close()

train_list.extend(test_list)

n_training=np.array(train_list)
n_testing=np.array(test_list)
n_training_X=n_training[:,0:6]
n_training_y=n_training[:,6]
n_testing_X=n_testing[:,0:6]
n_testing_y=list(n_testing[:,6])

clf_rbfg1=svm.SVC(kernel='rbf',gamma=(1.0/6.0)*1.0)
clf_rbfg1.fit(n_training_X,n_training_y)
n_predicted_y=list(clf_rbfg1.predict(n_testing_X))

tp=0.0
fp=0.0
fn=0.0
for i in range(0,len(n_testing_y)):
	if n_testing_y[i]==n_predicted_y[i]:
		tp+=1
	else:
		if n_predicted_y[i]==1:
			fp+=1
		else:
			fn+=1
P=tp/(tp+fp)
R=tp/(tp+fn)
F1=2*P*R/(P+R)

f=open("/Users/yalunzheng/Documents/BioPre/saliency/local/svmclf.pkl","wb")
pickle.dump(clf_rbfg1,f)
f.close()