import sys
import numpy as np
from time import time
from sklearn import svm

f=open("/home/ubuntu/results/coclf/trainlist.pkl","rb")
training_list=pickle.load(f)
f.close()

f=open("/home/ubuntu/results/coclf/testlist.pkl","rb")
testing_list=pickle.load(f)
f.close()

training_list.extend(testing_list)

clf_linear=svm.OneClassSVM(kernel='linear')
clf_rbf=svm.OneClassSVM(kernel='rbf')

n_training=np.array(training_list)

start=time()

clf_linear.fit(n_training)

end=time()

print(end-start)

start=time()

clf_rbf.fit(n_training)

end=time()

print(end-start)

f=open("/home/ubuntu/results/coclf/linear.pkl","wb")
pickle.dump(clf_linear,f)
f.close()

f=open("/home/ubuntu/results/coclf/rbf_default.pkl","wb")
pickle.dump(clf_rbf,f)
f.close()