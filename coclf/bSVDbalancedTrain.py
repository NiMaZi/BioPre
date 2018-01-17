import sys
import math
import random
import pickle
import numpy as np
from sklearn import svm

pos_list=[]
neg_prelist=[]

for chunk in range(0,1):
	f=open("/home/ubuntu/results/coclf/bsvd_trainlist"+str(chunk)+".pkl","rb")
	_list=pickle.load(f)
	f.close()
	for item in _list:
		if item[38]==1:
			pos_list.append(item)
		else:
			neg_prelist.append(item)

neg_list=random.sample(neg_prelist,len(pos_list))

pos_list.extend(neg_list)
train_list=list(pos_list)
random.shuffle(train_list)

n_train=np.array(train_list)
n_train_X=n_train[:,0:38]
n_train_y=n_train[:,38]

clf_linear=svm.LinearSVC()
clf_rbf=svm.SVC(gamma=1.0/38.0)

clf_linear.fit(n_train_X,n_train_y)
clf_rbf.fit(n_train_X,n_train_y)

f=open("/home/ubuntu/results/coclf/bsvd_linear.pkl","wb")
pickle.dump(clf_linear,f)
f.close()

f=open("/home/ubuntu/results/coclf/bsvd_rbf_default.pkl","wb")
pickle.dump(clf_rbf,f)
f.close()