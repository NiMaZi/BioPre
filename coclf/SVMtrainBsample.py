import sys
import math
import pickle
import random
import numpy as np
from sklearn import svm
from sklearn import linear_model as lm

split_ratio=float(sys.argv[1])

partial_volume=10000

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

pos_list=[]
neg_prelist=[]
count=0
clf_sgd=lm.SGDClassifier()

for i in range(0,int(len(featured_list)*split_ratio)):
	abs_dict=featured_list[i]['abs']
	body_dict=featured_list[i]['body']
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
				if b_key in body_dict.keys():
					label=1
					_list=[dev_mat[word_list.index(a_key_1)][word_list.index(b_key)],dev_mat[word_list.index(a_key_2)][word_list.index(b_key)]]
					_list.extend(word2tvec[a_key_1])
					_list.extend(word2tvec[a_key_2])
					_list.append(label)
					pos_list.append(_list)
					# pos_list.append([centrality[a_key_1],centrality[a_key_2],centrality[b_key],dev_mat[word_list.index(a_key_1)][word_list.index(b_key)],dev_mat[word_list.index(a_key_1)][word_list.index(b_key)],pred_saliency_1,pred_saliency_2,label])
				else:
					label=0
					_list=[dev_mat[word_list.index(a_key_1)][word_list.index(b_key)],dev_mat[word_list.index(a_key_2)][word_list.index(b_key)]]
					_list.extend(word2tvec[a_key_1])
					_list.extend(word2tvec[a_key_2])
					_list.append(label)
					neg_prelist.append(_list)
					# neg_prelist.append([centrality[a_key_1],centrality[a_key_2],centrality[b_key],dev_mat[word_list.index(a_key_1)][word_list.index(b_key)],dev_mat[word_list.index(a_key_1)][word_list.index(b_key)],pred_saliency_1,pred_saliency_2,label])
				# print(count,a_key_1,a_key_2,b_key,label)
				count+=1
	if count>partial_volume:
		sample_prelist=random.sample(neg_prelist,len(pos_list))
		sample_prelist.extend(pos_list)
		random.shuffle(sample_prelist)
		tlen=len(sample_prelist[0])

# print(len(sample_prelist))

# clf_linear=svm.LinearSVC()
# clf_rbf=svm.SVC(gamma=0.25)

# clf_lr=lm.LogisticRegression()


		nTrain=np.array(sample_prelist)
		nX=nTrain[:,0:tlen-1]
		ny=nTrain[:,tlen-1]

# clf_linear.fit(nX,ny)
# clf_rbf.fit(nX,ny)
# clf_lr.fit(nX,ny)
		clf_sgd.partial_fit(nX,ny,classes=[0,1])
		pos_list=[]
		neg_prelist=[]
		count=0

# f=open("/home/ubuntu/results/coclf/clf_linear.pkl","wb")
# pickle.dump(clf_linear,f)
# f.close()

# f=open("/home/ubuntu/results/coclf/clf_rbf.pkl","wb")
# pickle.dump(clf_rbf,f)
# f.close()

# f=open("/home/ubuntu/results/coclf/b_clf_lr.pkl","wb")
# pickle.dump(clf_lr,f)
# f.close()

f=open("/home/ubuntu/results/coclf/b_clf_sgd_test.pkl","wb")
pickle.dump(clf_sgd,f)
f.close()