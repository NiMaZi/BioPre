import sys
import math
import random
import pickle
import numpy as np
from sklearn import svm

pos_list=[]
neg_prelist=[]

for chunk in range(0,34):
	with open("/home/ubuntu/results/coclf/bsvd_trainlist"+str(chunk)+".pkl","rb") as f:
		_list=pickle.load(f)
		for item in _list:
			if item[38]==1:
				pos_list.append(item)
			else:
				neg_prelist.append(item)

neg_list=random.sample(neg_prelist,len(pos_list))

train_list=pos_list.extend(neg_list)
random.shuffle(train_list)

print(len(train_list))