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
from models.bownn import BOWNN
sys.stderr=stderr
os.environ['TF_CPP_MIN_LOG_LEVEL']='3'

parser=argparse.ArgumentParser(description='train.py')
parser.add_argument('-input',default='data_sample/ConCode2Vid.json',type=str,help="input dictionary")
parser.add_argument('-output',default='data_sample/ConCode2Vid.json',type=str,help="output dictionary")
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

def main():

	in_path=opt.input
	out_path=opt.output
	in_dict=util.load_sups(in_path)
	out_dict=util.load_sups(out_path)
	folder=opt.data
	volume=opt.volume
	save_path=opt.path
	
	bownn_model=BOWNN(len(in_dict),512,len(out_dict))
	bownn_model.build_model()

	train(bownn_model,folder,in_dict,out_dict,volume)

	bownn_model.save_model(save_path)

if __name__=='__main__':
	main()