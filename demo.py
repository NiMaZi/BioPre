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