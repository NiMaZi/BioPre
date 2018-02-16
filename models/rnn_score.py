import csv
import sys
import json
import numpy as np
from keras.models import load_model

def load_trained_model(_path):
	model=load_model(_path)
	return model

def decode(_vec,_dict):
	min_dist=np.inf
	target_word=''
	for w in _dict.keys():
		dist=np.linalg.norm(_vec-np.array(_dict[w]))
		if dist<min_dist:
			min_dist=dist
			target_word=w
	return target_word,min_dist

def sliding_window(_array,_size):
	return

def test_corpus(_offset,_volume,_chunk,_model):
	fp=open("/home/ubuntu/results_new/ontology/word2tvec.json",'r',encoding='utf-8')
	word2tvec=json.load(fp)
	fp.close()
	fp=open("/home/ubuntu/results_new/ontology/word_dict.json",'r',encoding='utf-8')
	word_dict=json.load(fp)
	fp.close()
	P_all=0.0
	for i in range(_offset,_offset+_volume):
		seq_list=[]
		wseq_list=[]
		time_steps=[]
		wtime_steps=[]
		abs_set=set()
		f=open("/home/ubuntu/thesiswork/kdata/abs"+str(i)+".csv",'r',encoding='utf-8')
		rd=csv.reader(f)
		for item in rd:
			if item[2]=="ConceptName":
				continue
			try:
				abs_set.add(item[1])
				time_steps.append(word2tvec[item[1]])
				wtime_steps.append(item[2])
			except:
				pass
			if len(time_steps)>=_chunk:
				seq_list.append(time_steps)
				wseq_list.append(wtime_steps)
				wtime_steps=[]
				time_steps=[]
		if time_steps:
			seq_list.append(time_steps)
			wseq_list.append(wtime_steps)
		for seq in seq_list:
			if len(seq)<_chunk:
				for i in range(0,_chunk-len(seq)):
					seq.append([-1.0 for i in range(0,len(seq[0]))])
		f.close()
		N_all=np.array(seq_list)
		X_in=N_all[:,:_chunk,:]
		y_out=_model.predict(X_in)
		res_list={}
		for p in y_out:
			word,dist=decode(p,word2tvec)
			res_list[word]=dist
		# print(res_list)
		body_set=set()
		f=open("/home/ubuntu/thesiswork/kdata/body"+str(i)+".csv",'r',encoding='utf-8')
		rd=csv.reader(f)
		for item in rd:
			if item[2]=="ConceptName":
				continue
			try:
				body_set.add(item[1])
			except:
				pass
		real_set=body_set-abs_set
		# print(real_set)
		tp=0.0
		fp=0.0
		fn=0.0
		for key in res_list.keys():
			if key in real_set:
				tp+=1.0
			else:
				fp+=1.0
		P=tp/(tp+fp)
		# print(P)
		P_all+=P
	P_all/=_volume
	return P_all
		# for p in range(0,y_out.shape[0]):
			# print(wseq_list[p])
			# print(word_dict[decode(y_out[p],word2tvec)]['entity_name'])

if __name__ == '__main__':
	offset=int(sys.argv[1])
	volume=int(sys.argv[2])
	path="/home/ubuntu/results_new/models/LSTM.h5"
	model=load_trained_model(path)
	chunk=model.layers[0].get_config()['batch_input_shape'][1]
	score=test_corpus(offset,volume,chunk,model)
	print(score)