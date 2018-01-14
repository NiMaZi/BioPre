import sys
import math
import pickle
import numpy as np
from sklearn import svm

split_ratio=float(sys.argv[1])

f=open("/home/ubuntu/results/saliency/featured.pkl","rb")
featured_list=pickle.load(f)
f.close()

f=open("/home/ubuntu/results/saliency/wordlist.pkl","rb")
word_list=pickle.load(f)
f.close()

f=open("/home/ubuntu/results/saliency/idf.pkl","rb")
idf=pickle.load(f)
f.close()

f=open("/home/ubuntu/results/saliency/centrality.pkl","rb")
centrality=pickle.load(f)
f.close()

f=open("/home/ubuntu/results/saliency/keyphrase.pkl","rb")
key_phrase=pickle.load(f)
f.close()

f=open("/home/ubuntu/results/saliency/svmclf.pkl","rb")
s_clf=pickle.load(f)
f.close()

sample_prelist=[]
count=0

for entry in featured_list:
	abs_dict=entry['abs']
	body_dict=entry['body']
	for a_key in abs_dict.keys():
		for b_key in body_dict.keys():
			if a_key==b_key:
				continue
			print(count,a_key,b_key)
			count+=1
			pred_input=np.array([[key_phrase[word_list.index(a_key)],abs_dict[a_key][0],abs_dict[a_key][1]-abs_dict[a_key][0],abs_dict[a_key][2],idf[word_list.index(a_key)],centrality[a_key]]])
			pred_saliency=list(s_clf.predict(pred_input))[0]
			sample_prelist.append([abs_dict[a_key][0],abs_dict[a_key][1]-abs_dict[a_key][0],abs_dict[a_key][2],idf[word_list.index(a_key)],centrality[a_key],idf[word_list.index(b_key)],centrality[b_key],pred_saliency])

split=int(split_ratio*len(sample_prelist))

training_list=[]
for i in range(0,split):
	training_list.append(sample_prelist[i])

f=open("/home/ubuntu/results/coclf/trainlist.pkl","wb")
pickle.dump(training_list,f)
f.close()

test_list=[]
for i in range(split,len(sample_prelist)):
	test_list.append(sample_prelist[i])

f=open("/home/ubuntu/results/coclf/testlist.pkl","wb")
pickle.dump(test_list,f)
f.close()