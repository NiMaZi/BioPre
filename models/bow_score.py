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

def get_model_S3(_name):
	bucket=get_bucket()
	homedir=os.environ['HOME']
	try:
		os.remove(homedir+"/temp/tmp_model.h5")
	except:
		pass
	bucket.download_file("yalun/results/models/"+_name+".h5",homedir+"/temp/tmp_model.h5")
	model=load_model(homedir+"/temp/tmp_model.h5")
	return model

def get_model_local(path):
	return load_model(path)

def test_on_doc_S3(_model,_volume,_threshold=0.0):
	homedir=os.environ['HOME']
	bucket=get_bucket()
	prefix,word_list=load_sups()
	sample_list=[]
	P_all=0.0
	R_all=0.0
	all_count=0.0
	for i in range(0,_volume):
		abs_vec=[0.0 for i in range(0,len(word_list))]
		abs_count=0.0
		bucket.download_file("yalun/annotated_papers_with_txt_new/abs"+str(i)+".csv",homedir+"/temp/tmp.csv")
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
		bucket.download_file("yalun/annotated_papers_with_txt_new/body"+str(i)+".csv",homedir+"/temp/tmp.csv")
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
		sample_list=[abs_vec+body_vec]
		N_test=np.array(sample_list)
		X_test=N_test[:,:len(word_list)]
		Y_test=np.ceil(N_test[:,len(word_list):])[0]
		Y_pred=_model.predict(X_test)[0]
		Y_pred/=np.linalg.norm(Y_pred)
		bset=set()
		for i,d in enumerate(list(Y_test)):
			if d>0:
				bset.add(i)
		pset=set()
		for i,d in enumerate(list(Y_pred)):
			if d>=threshold:
				pset.add(i)
		tp=float(len(bset&pset))
		fp=len(pset-bset)
		fn=len(bset-pset)
		try:
			P=tp/(tp+fp)
		except:
			P=0.0
		try:
			R=tp/(tp+fn)
		except:
			R=0.0
		P_all+=P
		R_all+=R
		all_count+=1
	P_all/=all_count
	R_all/=all_count
	try:
		F1=2*P_all*R_all/(P_all+R_all)
	except:
		F1=0.0
	return P_all,R_all,F1

if __name__=="__main__":
	homedir=os.environ['HOME']
	logf=open(homedir+"/results/logs/bow_score.txt",'a')
	model_name="temp_model_1hidden"
	volume=20
	logf.write("%s,%d\n"%(model_name,volume))
	# model=get_model_S3(model_name)
	model=get_model_local(homedir+"/results/models/"+model_name+".h5")
	threshold=0.0
	while threshold<0.2:
		P,R,F1=test_on_doc_S3(model,volume,threshold)
		logf.write("%.3f,%.3f,%.3f,%.3f\n"%(threshold,P,R,F1))
		print("%.3f,%.3f,%.3f,%.3f"%(threshold,P,R,F1))
		threshold+=0.01
	logf.close()