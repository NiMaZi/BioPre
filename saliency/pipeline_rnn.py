import csv
import sys
import json
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, SimpleRNN, Dense

def build_model(_input_dim,_input_length):
	model=Sequential()
	model.add(SimpleRNN(_input_dim,input_dim=_input_dim,input_length=_input_length,return_sequences=False,activation="relu"))
	model.compile(optimizer='rmsprop',loss='binary_crossentropy')
	return model

def build_data(_volume,_chunk,_split):
	fp=open("/home/ubuntu/results_new/ontology/word2tvec.json",'r',encoding='utf-8')
	word2tvec=json.load(fp)
	fp.close()
	seq_list=[]
	for i in range(0,_volume):
		time_steps=[]
		f=open("/home/ubuntu/thesiswork/kdata/body"+str(i)+".csv",'r',encoding='utf-8')
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
	N_train=N_all[:int(_split*len(seq_list)),:,:]
	N_test=N_all[int(_split*len(seq_list)):,:,:]
	X_train=N_train[:,:_chunk-1,:]
	y_train=N_train[:,_chunk-1,:]
	X_test=N_test[:,:_chunk-1,:]
	y_test=N_test[:,_chunk-1,:]
	input_dim=len(seq_list[0][0])
	input_length=len(seq_list[0])
	return X_train,y_train,X_test,y_test,input_dim,input_length

if __name__=="__main__":
	if len(sys.argv)<4:
		print("Usage: -volume -chunk-size -split-rate.\n")
		sys.exit(0)
	volume=int(sys.argv[1])
	chunk=int(sys.argv[2])
	split=float(sys.argv[3])
	X_train,y_train,X_test,y_test,input_dim,input_length=build_data(volume,chunk,split)
	model=build_model(input_dim,input_length)
	model.fit(X_train,y_train)
	score=model.evaluate(X_test,y_test)
	print(score)