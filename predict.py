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

parser=argparse.ArgumentParser(description='predict.py')
parser.add_argument('-input',default='data_sample/vocab/ConCode2Vid.json',type=str,help="input dictionary")
parser.add_argument('-output',default='data_sample/vocab/ConCode2Vid.json',type=str,help="output dictionary")
parser.add_argument('-author',default='data_sample/vocab/FAuthor2Vid.json',type=str,help="author dictionary")
parser.add_argument('-vocab',default='data_sample/vocab/Vid2Name.json',type=str,help="entity dictionary")
parser.add_argument('-A',default=False,type=bool,help="train with author info")
parser.add_argument('-E',default=False,type=bool,help="evaluate with real body")
parser.add_argument('-abstract',default='data_sample/sample/abs0.csv',type=str,help="abstract to predict")
parser.add_argument('-body',default='data_sample/sample/body0.csv',type=str,help="body to evaluate")
parser.add_argument('-path',default='model.h5',type=str,help="path for loading the model")
parser.add_argument('-threshold',default=0.0,type=float,help="threshold of prediction, 0.0~1.0")
opt=parser.parse_args()

def get_prediction(model,abs_path,in_dict):
	cc2vid_input=in_dict
	abs_vec=[0.0 for i in range(0,len(cc2vid_input))]
	abs_count=0.0

	with open(abs_path,'r',encoding='utf-8') as cf:
		rd=csv.reader(cf)
		for item in rd:
			if item[0]=="Mention":
				continue
			try:
				abs_vec[cc2vid_input[item[1]]]+=1.0
				abs_count+=1.0
			except:
				pass
	if not abs_count==0.0:
		abs_vec=list(np.array(abs_vec)/abs_count)

	pred=model.model.predict(np.array([abs_vec]))[0]
	pred/=np.linalg.norm(pred)

	return abs_vec,list(pred)


def get_prediction_author(model,abs_path,in_dict,author_dict):
	pass

def print_vec(prediction,entity_dict,threshold=0.0):
	for i,v in enumerate(prediction):
		if v>threshold:
			print(entity_dict[i],end=',')

def eval_prediction(prediction,body_path,out_dict):
	pass

def main():
	in_path=opt.input
	out_path=opt.output
	entity_path=opt.vocab
	in_dict=util.load_sups(in_path)
	out_dict=util.load_sups(out_path)
	entity_dict=util.load_sups(entity_path)
	abs_path=opt.abstract
	load_path=opt.path
	threshold=opt.threshold

	author=opt.A
	evaluate=opt.E

	if not author:
		bownn_model=BOWNN()
	else:
		bownn_model=BOWNN_author()

	bownn_model.load_model(load_path)
	abs_vec,prediction=get_prediction(bownn_model,abs_path,in_dict)
	print("Entity mentions in this abstract:")
	print_vec(abs_vec,entity_dict)
	print("\n")
	print("Entity mentions predicted:")
	print_vec(prediction,entity_dict,threshold)
	print("\n")

	if evaluate:
		body_path=opt.body
		eval_prediction(prediction,body_path,out_dict)

if __name__=='__main__':
	main()