import sys
import math
import random
import pickle
import numpy as np
from sklearn import svm
from sklearn import linear_model as lm

front_split_ratio=float(sys.argv[1])
end_split_ratio=float(sys.argv[2])
confidence=float(sys.argv[3])

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

f=open("/home/ubuntu/results/coclf/b_clf_lr.pkl","rb")
clf_lr=pickle.load(f)
f.close()

f=open("/home/ubuntu/results/coclf/b_clf_sgd_test.pkl","rb")
clf_sgd=pickle.load(f)
f.close()

count=0

# tp_linear=0.0
# fp_linear=0.0
# fn_linear=0.0
tp_rbf=0.0
fp_rbf=0.0
fn_rbf=0.0
log_list=[]

# for i in range(int(front_split_ratio*len(featured_list)),int(end_split_ratio*len(featured_list))):
for i in range(int(front_split_ratio*len(featured_list)),int(front_split_ratio*len(featured_list))+100):
	abs_dict=featured_list[i]['abs']
	body_dict=featured_list[i]['body']
	# max_conf_linear=0
	max_conf_rbf=0
	# pred_dict_linear={}
	pred_dict_rbf={}
	for a_key_1 in abs_dict.keys():
		for a_key_2 in abs_dict.keys():
			if a_key_1==a_key_2:
				continue
			if not a_key_1 in word_list or not a_key_2 in word_list:
				continue
			# pred_input=np.array([[key_phrase[word_list.index(a_key_1)],abs_dict[a_key_1][0],abs_dict[a_key_1][1]-abs_dict[a_key_1][0],abs_dict[a_key_1][2],idf[word_list.index(a_key_1)],centrality[a_key_1]],[key_phrase[word_list.index(a_key_2)],abs_dict[a_key_2][0],abs_dict[a_key_2][1]-abs_dict[a_key_2][0],abs_dict[a_key_2][2],idf[word_list.index(a_key_2)],centrality[a_key_2]]])
			# pred_saliency_1=list(s_clf.predict(pred_input))[0]
			# pred_saliency_2=list(s_clf.predict(pred_input))[1]
			for b_key in word_list:
				if a_key_1==b_key or a_key_2==b_key:
					continue
				count+=1
				if count>20000:
					outlog=random.sample(log_list,100)
					for l in outlog:
						print(l[0],l[1],l[2],l[3],l[4])
					sys.exit(0)
				label=0
				if b_key in body_dict.keys():
					label=1
				else:
					label=0
				_list=[dev_mat[word_list.index(a_key_1)][word_list.index(b_key)],dev_mat[word_list.index(a_key_2)][word_list.index(b_key)]]
				_list.extend(word2tvec[a_key_1])
				_list.extend(word2tvec[a_key_2])
				# _list.append(label)
				# print(count,a_key_1,a_key_2,b_key,label)
				sample_input=np.array([_list])

				# pred_label_linear=list(clf_lr.predict(sample_input))[0]
				# if pred_label_linear==1:
				# 	if b_key in pred_dict_linear.keys():
				# 		pred_dict_linear[b_key]+=1.0
				# 		if pred_dict_linear[b_key]>max_conf_linear:
				# 			max_conf_linear=pred_dict_linear[b_key]
				# 	else:
				# 		pred_dict_linear[b_key]=1.0
				# 		if pred_dict_linear[b_key]>max_conf_linear:
				# 			max_conf_linear=pred_dict_linear[b_key]

				pred_label_rbf=list(clf_sgd.predict(sample_input))[0]
				log_list.append([pred_label_rbf,label,a_key_1,a_key_2,b_key])
				if pred_label_rbf==1:
					if b_key in pred_dict_rbf.keys():
						pred_dict_rbf[b_key]+=1.0
						if pred_dict_rbf[b_key]>max_conf_rbf:
							max_conf_rbf=pred_dict_rbf[b_key]
					else:
						pred_dict_rbf[b_key]=1.0
						if pred_dict_rbf[b_key]>max_conf_rbf:
							max_conf_rbf=pred_dict_rbf[b_key]

	# for key in pred_dict_linear.keys():
	# 	pred_dict_linear[key]/=max_conf_linear

	for key in pred_dict_rbf.keys():
		pred_dict_rbf[key]/=max_conf_rbf

	# pred_set_linear=set()
	pred_set_rbf=set()

	# for key in pred_dict_linear.keys():
	# 	if pred_dict_linear[key]>confidence:
	# 		pred_set_linear.add(key)

	for key in pred_dict_rbf.keys():
		if pred_dict_rbf[key]>confidence:
			pred_set_rbf.add(key)

	real_set=set(body_dict.keys())-set(abs_dict.keys())
	# tp_linear+=len(pred_set_linear&real_set)
	# fp_linear+=len(pred_set_linear-(pred_set_linear&real_set))
	# fn_linear+=len(real_set-(real_set&pred_set_linear))
	tp_rbf+=len(pred_set_rbf&real_set)
	fp_rbf+=len(pred_set_rbf-(pred_set_rbf&real_set))
	fn_rbf+=len(real_set-(real_set&pred_set_rbf))


# P=tp_linear/(tp_linear+fp_linear)
# R=tp_linear/(tp_linear+fn_linear)
# F1=2*P*R/(P+R)

# print(P,R,F1)

P=tp_rbf/(tp_rbf+fp_rbf)
R=tp_rbf/(tp_rbf+fn_rbf)
F1=2*P*R/(P+R)

f=open("/home/ubuntu/results/coclf/sgd_test_log.txt","a")
f.write(str(confidence)+","+str(P)+","+str(R)+","+str(F1)+"\n")
f.close()