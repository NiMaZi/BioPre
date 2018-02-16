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

def test_corpus(_offset,_volume,_chunk,_model):
	fp=open("/home/ubuntu/results_new/ontology/word2tvec.json",'r',encoding='utf-8')
	word2tvec=json.load(fp)
	fp.close()
	fp=open("/home/ubuntu/results_new/ontology/word_dict.json",'r',encoding='utf-8')
	word_dict=json.load(fp)
	fp.close()
	for i in range(_offset,_offset+_volume):
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
		N_all=np.array(seq_list)
		print(N_all.shape)
		X_in=N_all[:,:_chunk,:]
		print(X_in.shape)
		y_out=_model.predict(X_in)
		print(y_out.shape)
		# for p in range(0,y_out.shape[0]):
			# print(wseq_list[p])
			# print(word_dict[decode(y_out[p],word2tvec)]['entity_name'])

if __name__ == '__main__':
	offset=int(sys.argv[1])
	volume=int(sys.argv[2])
	path="/home/ubuntu/results_new/models/LSTM.h5"
	model=load_trained_model(path)
	chunk=model.layers[0].get_config()['batch_input_shape'][1]
	test_corpus(offset,volume,chunk,model)