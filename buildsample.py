import pickle
import sys
import numpy as np
from sklearn import svm

volume=int(sys.argv[1])

f=open("/home/ubuntu/results/tfidf/tfidf2700.pickle","rb")
tf_idf=pickle.load(f)
f.close()

f=open("/home/ubuntu/results/tfidf/wordlist2700.pickle","rb")
word_list=pickle.load(f)
f.close()

f=open("/home/ubuntu/results/initDict.pickle","rb")
article_list=pickle.load(f)
f.close()

f=open("/home/ubuntu/results/collectiveDict.pickle","rb")
cooc_dict=pickle.load(f)
f.close()

samples=[]

for i in range(0,volume):
	abs_mention=article_list[i]['abs'].keys()
	body_mention=article_list[i]['body'].keys()
	for a in abs_mention:
		for b in body_mention:
			if a==b:
				continue
			tf_idf_a=tf_idf[word_list.index(a)][i]
			tf_idf_b=tf_idf[word_list.index(b)][i]
			cooc=cooc_dict[a][b]
			samples.append([tf_idf_a,tf_idf_b,cooc])

print(np.array(samples))
print(len(samples))

clf=svm.OneClassSVM(kernel="linear")
clf.fit(np.array(samples))
predy=clf.predict(np.array(samples))

print(predy)