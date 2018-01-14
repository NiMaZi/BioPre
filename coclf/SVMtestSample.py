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

f=open("/home/ubuntu/results/saliency/simplemat.pkl","rb")
dev_mat=pickle.load(f)
f.close()

f=open("/home/ubuntu/results/coclf/linear.pkl","rb")
clf_linear=pickle.load(f)
f.close()

f=open("/home/ubuntu/results/coclf/rbf_default.pkl","rb")
clf_rbf=pickle.load(f)
f.close()

sample_prelist=[]
count=0

tp_linear=0.0
fp_linear=0.0
fn_linear=0.0
tp_rbf=0.0
fp_rbf=0.0
fn_rbf=0.0

for entry in featured_list:
	abs_dict=entry['abs']
	body_dict=entry['body']
	for a_key in abs_dict.keys():
		pred_input=np.array([[key_phrase[word_list.index(a_key)],abs_dict[a_key][0],abs_dict[a_key][1]-abs_dict[a_key][0],abs_dict[a_key][2],idf[word_list.index(a_key)],centrality[a_key]]])
		pred_saliency=list(s_clf.predict(pred_input))[0]
		for b_key in word_list:
			if a_key==b_key:
				continue
			count+=1
			if count>20000:
				break
			label=0
			if b_key in body_dict.keys():
				label=1
			else:
				label=-1
			print(count,a_key,b_key,label)
			sample_input=np.array([[abs_dict[a_key][0],abs_dict[a_key][1]-abs_dict[a_key][0],abs_dict[a_key][2],idf[word_list.index(a_key)],centrality[a_key],idf[word_list.index(b_key)],centrality[b_key],pred_saliency]])
			pred_label_linear=list(clf_linear.predict(sample_input))[0]
			pred_label_rbf=list(clf_rbf.predict(sample_input))[0]
			if pred_label_linear==label:
				tp_linear+=1
			else:
				if pred_label_linear==1:
					fp_linear+=1
				else:
					fn_linear+=1
			if pred_label_rbf==label:
				tp_rbf+=1
			else:
				if pred_label_rbf==1:
					fp_rbf+=1
				else:
					fn_rbf+=1
			# sample_prelist.append([abs_dict[a_key][0],abs_dict[a_key][1]-abs_dict[a_key][0],abs_dict[a_key][2],idf[word_list.index(a_key)],centrality[a_key],idf[word_list.index(b_key)],centrality[b_key],pred_saliency,label])

P=tp_linear/(tp_linear+fp_linear)
R=tp_linear/(tp_linear+fn_linear)
F1=2*P*R/(P+R)

print(P,R,F1)

P=tp_rbf/(tp_rbf+fp_rbf)
R=tp_rbf/(tp_rbf+fn_rbf)
F1=2*P*R/(P+R)

print(P,R,F1)

# f=open("/home/ubuntu/results/coclf/testlist.pkl","wb")
# pickle.dump(sample_prelist,f)
# f.close()