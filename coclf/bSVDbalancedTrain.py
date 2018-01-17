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

print(pos_list)
print(neg_list)

neg_list=random.sample(neg_prelist,len(pos_list))

train_list=list(pos_list.extend(neg_list))
random.shuffle(train_list)

print(len(train_list))