import sys
import math
import pickle
import numpy as np
from sklearn import linear_model as lm

front_split_ratio=float(sys.argv[1])
end_split_ratio=float(sys.argv[2])
# confidence=float(sys.argv[3])

def tree_distance(vec_1,vec_2):
	distance=0.0
	for i in range(0,len(vec_1)):
		if not vec_1[i]==vec_2[i]:
			for j in range(i,len(vec_1)):
				if vec_1[j]==-1.0:
					break
				distance+=1.0
			for j in range(i,len(vec_2)):
				if vec_2[j]==-1.0:
					break
				distance+=1.0
	return distance

f=open("/home/ubuntu/results/saliency/featured.pkl","rb")
featured_list=pickle.load(f)
f.close()

f=open("/home/ubuntu/results/ontology/ontology_wordlist.pkl","rb")
word_list=pickle.load(f)
f.close()

f=open("/home/ubuntu/results/ontology/ontology_word2taxonomy.pkl","rb")
word2tvec=pickle.load(f)
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

f=open("/home/ubuntu/results/coclf/b_clf_sgd_plusdis_minusvec.pkl","rb")
clf_sgd=pickle.load(f)
f.close()

confidence=0.0
while confidence<1.0:
	tp_rbf=0.0
	fp_rbf=0.0
	fn_rbf=0.0
	for i in range(int(front_split_ratio*len(featured_list)),int(end_split_ratio*len(featured_list))):
		abs_dict=featured_list[i]['abs']
		body_dict=featured_list[i]['body']
		max_conf_rbf=0
		pred_dict_rbf={}
		abs_key_list=list(abs_dict.keys())
		for i1 in range(0,len(abs_key_list)):
			for i2 in range(i1,len(abs_key_list)):
				a_key_1=abs_key_list[i1]
				a_key_2=abs_key_list[i2]
				if a_key_1==a_key_2:
					continue
				if not a_key_1 in word_list or not a_key_2 in word_list:
					continue
				for b_key in word_list:
					if a_key_1==b_key or a_key_2==b_key:
						continue
					a1_tvec=b_word2tvec[a_key_1]
					a2_tvec=b_word2tvec[a_key_2]
					b_tvec=b_word2tvec[b_key]
					disa1a2=tree_distance(a1_tvec,a2_tvec)
					disa1b=tree_distance(a1_tvec,b_tvec)
					disa2b=tree_distance(a2_tvec,b_tvec)
					try:
						_list=[dev_mat[word_list.index(a_key_1)][word_list.index(b_key)],dev_mat[word_list.index(a_key_2)][word_list.index(b_key)]]
					except:
						_list=[0.0,0.0]
					_list.extend([disa1a2,disa1b,disa2b])
					sample_input=np.array([_list])
					pred_label_rbf=list(clf_sgd.predict(sample_input))[0]
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
		real_set=set(body_dict.keys())-set(abs_dict.keys())
		tp_rbf+=len(pred_set_rbf&real_set)
		fp_rbf+=len(pred_set_rbf-(pred_set_rbf&real_set))
		fn_rbf+=len(real_set-(real_set&pred_set_rbf))
	try:
		P=tp_rbf/(tp_rbf+fp_rbf)
	except:
		P=0.0
	try:
		R=tp_rbf/(tp_rbf+fn_rbf)
	except:
		R=0.0
	try:
		F1=2*P*R/(P+R)
	except:
		F1=0.0
	f=open("/home/ubuntu/results/coclf/sgd_test_log_plusdis_minusvec.txt","a")
	f.write(str(confidence)+","+str(P)+","+str(R)+","+str(F1)+"\n")
	f.close()
	confidence+=0.1