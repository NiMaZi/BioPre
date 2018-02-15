import csv
import sys
import json
import numpy as np
from keras.models import load_model

def load_trained_model(_path):
	model=load_model(_path)
	return model

def decode(_vec):
	min_dist=np.inf
	target_word=''
	for w in word2tvec.keys():
		dist=np.linalg.norm(_vec,np.array(word2tvec[w]))
		if dist<min_dist:
			min_dist=dist
			target_word=w
	return w

def test_corpus(_offset,_volume,_chunk,_model):
	fp=open("/home/ubuntu/results_new/ontology/word2tvec.json",'r',encoding='utf-8')
	word2tvec=json.load(fp)
	fp.close()
	for i in range(_offset,_volume):
		seq_list=[]
		wseq_list=[]
		time_steps=[]
		wtime_steps=[]
		f=open("/home/ubuntu/thesiswork/kdata/abs"+str(i)+".csv",'r',encoding='utf-8')
		rd=csv.reader(f)
		for item in rd:
			if item[2]=="ConceptName":
				continue
			try:
				time_steps.append(word2tvec[item[1]])
			except:
				pass
			if len(time_steps)>=_chunk:
				seq_list.append(time_steps)
				time_steps=[]
		if time_steps:
			seq_list.append(time_steps)
		for seq in seq_list:
			if len(seq)<_chunk:
				for i in range(0,_chunk-len(seq)):
					seq.append([-1.0 for i in range(0,len(seq[0]))])
		N_all=np.array(seq_list)
		X_in=N_all[:,:_chunk-1,:]
		y_out=_model.predict(X_in)
		print(y_out.shape)

if __name__ == '__main__':
	offset=int(sys.argv[1])
	volume=int(sys.argv[2])
	path="/home/ubuntu/results_new/models/SimpleRNN.h5"
	model=load_trained_model(path)
	test_corpus(offset,volume,10,model)