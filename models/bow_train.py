import os
import sys
import csv
import json
import boto3
import numpy as np
from keras.models import Sequential,load_model
from keras.layers import Dense,Dropout,BatchNormalization
from keras.callbacks import EarlyStopping

def get_bucket():
	s3 = boto3.resource("s3")
	myBucket=s3.Bucket('workspace.scitodate.com')
	return myBucket

def load_sups():
	homedir=os.environ['HOME']
	f=open(homedir+"/results/ontology/full_word_list.json",'r')
	word_list=json.load(f)
	f.close()
	prefix='http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#'
	return prefix,word_list[1:]

def build_model(_input_dim=133609,_hidden_dim=512,_drate=0.5):
	model=Sequential()
	model.add(Dense(_hidden_dim,input_shape=(_input_dim,),activation='relu'))
	model.add(Dropout(_drate))
	model.add(BatchNormalization())
	model.add(Dense(_input_dim,activation='relu'))
	model.compile(optimizer='nadam',loss='binary_crossentropy')
	return model

def train_on_batch_S3(_model,_volume,_batch,_mbatch,_epochs=5):
	early_stopping=EarlyStopping(monitor='loss',patience=2)
	early_stopping_val=EarlyStopping(monitor='val_loss',patience=2)
	homedir=os.environ['HOME']
	bucket=get_bucket()
	prefix,word_list=load_sups()
	sample_list=[]
	batch_count=0
	for i in range(0,_volume):
		abs_vec=[0.0 for i in range(0,len(word_list))]
		abs_count=0.0
		bucket.download_file("yalun/annotated_papers_with_txt/abs"+str(i)+".csv",homedir+"/temp/tmp.csv")
		with open(homedir+"/temp/tmp.csv",'r',encoding='utf-8') as cf:
			rd=csv.reader(cf)
			for item in rd:
				if item[0]=="Mention":
					continue
				abs_count+=1.0
				abs_vec[word_list.index(prefix+item[1])]+=1.0
		if not abs_count:
			continue
		abs_vec=list(np.array(abs_vec)/abs_count)
		body_vec=[0.0 for i in range(0,len(word_list))]
		body_count=0.0
		bucket.download_file("yalun/annotated_papers_with_txt/body"+str(i)+".csv",homedir+"/temp/tmp.csv")
		with open(homedir+"/temp/tmp.csv",'r',encoding='utf-8') as cf:
			rd=csv.reader(cf)
			for item in rd:
				if item[0]=="Mention":
					continue
				body_count+=1.0
				body_vec[word_list.index(prefix+item[1])]+=1.0
		if not body_count:
			continue
		body_vec=list(np.array(abs_vec)/body_count)
		sample_list.append(abs_vec+body_vec)
		if len(sample_list)>=_batch:
			N_all=np.array(sample_list)
			X_train=N_all[:,:len(word_list)]
			Y_train=np.ceil(N_all[:,len(word_list):])
			_model.fit(X_train,Y_train,shuffle=True,batch_size=_mbatch,verbose=0,epochs=_epochs,validation_split=1.0/16.0,callbacks=[early_stopping,early_stopping_val])
			try:
				os.remove(homedir+"/temp/tmp_model.h5")
			except:
				pass
			_model.save(homedir+"/temp/tmp_model.h5")
			s3f=open(homedir+"/temp/tmp_model.h5",'rb')
			updata=s3f.read()
			bucket.put_object(Body=updata,Key="yalun/results/models/MLPsparse_1hidden_"+str(batch_count)+".h5")
			s3f.close()
			batch_count+=1
			sample_list=[]
	if len(sample_list):
		N_all=np.array(sample_list)
		X_train=N_all[:,:len(word_list)]
		Y_train=np.ceil(N_all[:,len(word_list):])
		_model.fit(X_train,Y_train,shuffle=True,batch_size=_mbatch,verbose=0,epochs=_epochs,validation_split=1.0/16.0,callbacks=[early_stopping,early_stopping_val])
		try:
			os.remove(homedir+"/temp/tmp_model.h5")
		except:
			pass
		_model.save(homedir+"/temp/tmp_model.h5")
		s3f=open(homedir+"/temp/tmp_model.h5",'rb')
		updata=s3f.read()
		bucket.put_object(Body=updata,Key="yalun/results/models/MLPsparse_1hidden_"+str(batch_count)+".h5")
		s3f.close()
		batch_count+=1
	return batch_count

if __name__=="__main__":
	model=build_model()
	total=train_on_batch_S3(model,10000,272,256)