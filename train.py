import warnings
warnings.filterwarnings("ignore")

import os
import sys

stderr=sys.stderr
sys.stderr=open(os.devnull,'w')
import csv
import argparse
import numpy as np
from utils import util
from models.bownn import BOWNN,BOWNN_author
sys.stderr=stderr
os.environ['TF_CPP_MIN_LOG_LEVEL']='3'

parser=argparse.ArgumentParser(description='train.py')
parser.add_argument('-input',default='data_sample/vocab/ConCode2Vid.json',type=str,help="input dictionary")
parser.add_argument('-output',default='data_sample/vocab/ConCode2Vid.json',type=str,help="output dictionary")
parser.add_argument('-author',default='data_sample/vocab/FAuthor2Vid.json',type=str,help="author dictionary")
parser.add_argument('-A',default=False,type=bool,help="train with author info")
parser.add_argument('-data',default='data_sample/sample',type=str,help="training data directory")
parser.add_argument('-volume',default=1024,type=int,help="training data size")
parser.add_argument('-path',default='model.h5',type=str,help="path for saving the model")
opt=parser.parse_args()

def train(model,folder,in_dict,out_dict,volume,batch_size=1024,epochs=5):
	cc2vid_input=in_dict
	cc2vid_output=out_dict
	sample_list=[]

	for i in range(0,volume):
		abs_vec=[0.0 for i in range(0,len(cc2vid_input))]
		abs_count=0.0

		with open(folder+"/abs"+str(i)+".csv",'r',encoding='utf-8') as cf:
			rd=csv.reader(cf)
			for item in rd:
				if item[0]=="Mention":
					continue
				try:
					abs_vec[cc2vid_input[item[1]]]+=1.0
					abs_count+=1.0
				except:
					pass
		if not abs_count:
			continue

		abs_vec=list(np.array(abs_vec)/abs_count)

		body_vec=[0.0 for i in range(0,len(cc2vid_output))]
		body_count=0.0

		with open(folder+"/body"+str(i)+".csv",'r',encoding='utf-8') as cf:
			rd=csv.reader(cf)
			for item in rd:
				if item[0]=="Mention":
					continue
				try:
					body_vec[cc2vid_output[item[1]]]+=1.0
					body_count+=1.0
				except:
					pass
		if not body_count:
			continue

		body_vec=list(np.array(body_vec)/body_count)
		sample_list.append(abs_vec+body_vec)

		if len(sample_list)>=batch_size:
			N_all=np.array(sample_list)
			X_train=N_all[:,:len(cc2vid_input)]
			Y_train=np.clip(np.ceil(N_all[:,len(cc2vid_input):])-np.ceil(X_train),0.0,1.0)
			model.model.fit(X_train,Y_train,batch_size=batch_size,verbose=0,epochs=epochs)
			sample_list=[]
	
	if len(sample_list):
		N_all=np.array(sample_list)
		X_train=N_all[:,:len(cc2vid_input)]
		Y_train=np.clip(np.ceil(N_all[:,len(cc2vid_input):])-np.ceil(X_train),0.0,1.0)
		model.model.fit(X_train,Y_train,batch_size=batch_size,verbose=0,epochs=epochs)

def train_author(model,folder,in_dict,author_dict,out_dict,volume,batch_size=1024,epochs=5):
	cc2vid_input=in_dict
	fa2vid=author_dict
	cc2vid_output=out_dict
	sample_list=[]

	for i in range(0,volume):
		abs_vec=[0.0 for i in range(0,len(cc2vid_input))]
		abs_count=0.0

		with open(folder+"/abs"+str(i)+".csv",'r',encoding='utf-8') as cf:
			rd=csv.reader(cf)
			for item in rd:
				if item[0]=="Mention":
					continue
				try:
					abs_vec[cc2vid_input[item[1]]]+=1.0
					abs_count+=1.0
				except:
					pass
		if not abs_count:
			continue

		abs_vec=list(np.array(abs_vec)/abs_count)

		author_vec=[0.0 for i in range(0,len(fa2vid))]

		tmpf=open(folder+"/authors"+str(i)+".json",'r',encoding='utf-8')
		authors=json.load(tmpf)
		tmpf.close()
		for author in authors:
			try:
				author_vec[fa2vid[author]]=1.0
			except:
				pass

		body_vec=[0.0 for i in range(0,len(cc2vid_output))]
		body_count=0.0

		with open(folder+"/body"+str(i)+".csv",'r',encoding='utf-8') as cf:
			rd=csv.reader(cf)
			for item in rd:
				if item[0]=="Mention":
					continue
				try:
					body_vec[cc2vid_output[item[1]]]+=1.0
					body_count+=1.0
				except:
					pass
		if not body_count:
			continue

		body_vec=list(np.array(body_vec)/body_count)
		sample_list.append(abs_vec+author_vec+body_vec)

		if len(sample_list)>=batch_size:
			N_all=np.array(sample_list)
			X_train_1=N_all[:,:len(cc2vid_input)]
			X_train_2=N_all[:,len(cc2vid_input):len(cc2vid_input)+len(fa2vid)]
			Y_train=np.clip(np.ceil(N_all[:,len(cc2vid_input)+len(fa2vid):])-np.ceil(X_train_1),0.0,1.0)
			model.model.fit([X_train_1,X_train_2],[Y_train],batch_size=batch_size,verbose=0,epochs=epochs)
			sample_list=[]
	
	if len(sample_list):
		N_all=np.array(sample_list)
		X_train_1=N_all[:,:len(cc2vid_input)]
		X_train_2=N_all[:,len(cc2vid_input):len(cc2vid_input)+len(fa2vid)]
		Y_train=np.clip(np.ceil(N_all[:,len(cc2vid_input)+len(fa2vid):])-np.ceil(X_train_1),0.0,1.0)
		model.model.fit([X_train_1,X_train_2],[Y_train],batch_size=batch_size,verbose=0,epochs=epochs)

def main():
	in_path=opt.input
	out_path=opt.output
	in_dict=util.load_sups(in_path)
	out_dict=util.load_sups(out_path)
	folder=opt.data
	volume=opt.volume
	save_path=opt.path

	author=opt.A
	if not author:
		bownn_model=BOWNN(len(in_dict),512,len(out_dict))
		bownn_model.build_model()
		train(bownn_model,folder,in_dict,out_dict,volume)
	else:
		author_path=opt.author
		author_dict=util.load_sups(author_path)
		bownn_model=BOWNN_author(len(in_dict),len(author_dict),512,len(out_dict))
		bownn_model.build_model()
		train_author(bownn_model,folder,in_dict,author_dict,out_dict,volume)

	bownn_model.save_model(save_path)

if __name__=='__main__':
	main()