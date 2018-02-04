import sys
import math
import pickle
import random
import numpy as np
from sklearn import svm
from sklearn import linear_model as lm

test_mode=int(sys.argv[1])
article_id=int(sys.argv[2])
cor_rate=float(sys.argv[3])
confidence=float(sys.argv[4])

f=open("/home/ubuntu/results/saliency/featured.pkl","rb")
featured_list=pickle.load(f)
f.close()

abs_dict=featured_list[article_id]['abs']
body_dict=featured_list[article_id]['body']

print("entities mentioned in the abstract:\n")

for key in abs_dict.keys():
	print(key+" ")

print("\nentities mentioned in the body:\n")

for key in body_dict.keys():
	print(key+" ")

print("\nentities predicted:\n")

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

f=open("/home/ubuntu/results/saliency/simplemat.pkl","rb")
dev_mat=pickle.load(f)
f.close()

f=open("/home/ubuntu/results/coclf/clf_lr.pkl","rb")
clf_lr=pickle.load(f)
f.close()

f=open("/home/ubuntu/results/coclf/clf_sgd.pkl","rb")
clf_sgd=pickle.load(f)
f.close()

f=open("/home/ubuntu/results/coclf/clf_sgd_correction.pkl","rb")
clf_sgd_correction=pickle.load(f)
f.close()

f=open("/home/ubuntu/results/coclf/clf_sgd_filter.pkl","rb")
clf_sgd_filter=pickle.load(f)
f.close()

pred_dict_rbf={}
max_conf_rbf=0
for a_key in abs_dict.keys():
	if a_key in word_list:
		a_key_phrase=key_phrase[word_list.index(a_key)]
		a_idf=word_list.index(a_key)
	else:
		a_key_phrase=0.0
		a_idf=0.0
	if a_key in centrality.keys():
		a_centrality=centrality[a_key]
	else:
		a_centrality=0.0
	pred_input=np.array([[a_key_phrase,abs_dict[a_key][0],abs_dict[a_key][1]-abs_dict[a_key][0],abs_dict[a_key][2],a_idf,a_centrality]])
	pred_saliency=list(s_clf.predict(pred_input))[0]
	for b_key in word_list:
		if a_key==b_key:
			continue
		if b_key in centrality.keys():
			b_centrality=centrality[b_key]
		else:
			b_centrality=0.0
		if a_key in word_list and b_key in word_list:
			dev_cor=dev_mat[word_list.index(a_key)][word_list.index(b_key)]
		else:
			dev_cor=0.0
		sample_input=np.array([[a_centrality,b_centrality,dev_cor,pred_saliency]])
		pred_label_rbf=list(clf_sgd.predict(sample_input))[0]
		if pred_label_rbf==1:
			pred_label_correction=list(clf_sgd_correction.predict(sample_input))[0]
			pred_label_filter=list(clf_sgd_filter.predict(sample_input))[0]
			pred_label_rbf=cor_rate*pred_label_correction+(1.0-cor_rate)*pred_label_filter
			if pred_label_rbf>0.5:
				pred_label_rbf=1
			else:
				pred_label_rbf=0
		if pred_label_rbf==1:
			if b_key in pred_dict_rbf.keys():
				pred_dict_rbf[b_key]+=1.0
				if pred_dict_rbf[b_key]>max_conf_rbf:
					max_conf_rbf=pred_dict_rbf[b_key]
			else:
				pred_dict_rbf[b_key]=1.0
				if pred_dict_rbf[b_key]>max_conf_rbf:
					max_conf_rbf=pred_dict_rbf[b_key]
for key in pred_dict_rbf.keys():
	pred_dict_rbf[key]/=max_conf_rbf
pred_set_rbf=set()
for key in pred_dict_rbf.keys():
	if pred_dict_rbf[key]>confidence:
		pred_set_rbf.add(key)

for entity in pred_set_rbf:
	print(entity+" ")