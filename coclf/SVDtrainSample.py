import sys
import math
import pickle
import numpy as np
from sklearn import svm

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
	a_mat=[]
	for a_key in abs_dict.keys():
		pred_input=np.array([[key_phrase[word_list.index(a_key)],abs_dict[a_key][0],abs_dict[a_key][1]-abs_dict[a_key][0],abs_dict[a_key][2],idf[word_list.index(a_key)],centrality[a_key]]])
		pred_saliency=list(s_clf.predict(pred_input))[0]
		a_mat.append([abs_dict[a_key][0],abs_dict[a_key][1]-abs_dict[a_key][0],abs_dict[a_key][2],idf[word_list.index(a_key)],centrality[a_key],pred_saliency])
	U,S,V=np.linalg.svd(np.array(a_mat),full_matrices=True)
	for b_key in body_dict.keys():
		if b_key in abs_dict.keys():
			continue
		print(count,abs_dict.keys(),b_key)
		sample_prelist.append([idf[word_list.index(b_key)],centrality[b_key]].extend(list(V.flatten())))

f=open("/home/ubuntu/results/coclf/svd_trainlist.pkl","wb")
pickle.dump(sample_prelist,f)
f.close()