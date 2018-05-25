import warnings
warnings.filterwarnings("ignore")

import os
import sys

stderr=sys.stderr
sys.stderr=open(os.devnull, 'w')
import csv
import argparse
import numpy as np
from utils import util
from models.bownn import BOWNN
sys.stderr=stderr

parser=argparse.ArgumentParser(description='train.py')
parser.add_argument('-input',default='cc2vid.json',type=str,help="input dictionary")
parser.add_argument('-output',default='cc2vid.json',type=str,help="output dictionary")
parser.add_argument('-data',default='data',type=str,help="training data folder")
parser.add_argument('-volume',default=1024,type=int,help="training data size")
opt=parser.parse_args()

def train(model,folder,in_dict,out_dict,volume,batch_size=1024,epochs=5):
	cc2vid_input=util.load_sups(in_dict)
	cc2vid_output=util.load_sups(out_dict)
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
					abs_vec[cc2vid[item[1]]]+=1.0
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
					body_vec[cc2vid[item[1]]]+=1.0
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
	print(opt.input)
	print(opt.output)
	print(opt.data)
	print(opt.volume)
	"""get arguments"""
	"""intialize model"""
	# train()

if __name__=='__main__':
	main()