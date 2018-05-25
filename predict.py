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
parser.add_argument('-abstract',default='data_sample/sample_author/abs0.csv',type=str,help="abstract to predict")
parser.add_argument('-authors',default='data_sample/sample_author/authors0.json',type=str,help="author information")
parser.add_argument('-body',default='data_sample/sample_author/body0.csv',type=str,help="body to evaluate")
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


def get_prediction_author(model,abs_path,authors_path,in_dict,author_dict):
	cc2vid_input=in_dict
	fa2vid=author_dict

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

	author_vec=[0.0 for i in range(0,len(fa2vid))]
	authors=util.load_sups(authors_path)
	for author in authors:
		try:
			author_vec[fa2vid[author]]=1.0
		except:
			pass

	sample_input=np.array([abs_vec+author_vec])
	pred=model.model.predict([sample_input[:,:len(cc2vid_input)],sample_input[:,len(cc2vid_input):]])[0]
	pred/=np.linalg.norm(pred)

	return abs_vec,list(pred)

def print_vec(prediction,entity_dict,threshold=0.0):
	for i,v in enumerate(prediction):
		if v>threshold:
			try:
				print(entity_dict[i],end=',')
			except:
				pass

def eval_prediction(prediction,body_path,out_dict,threshold=0.0):
	cc2vid_output=out_dict
	body_vec=[0.0 for i in range(0,len(cc2vid_output))]

	with open(body_path,'r',encoding='utf-8') as cf:
		rd=csv.reader(cf)
		for item in rd:
			if item[0]=="Mention":
				continue
			try:
				body_vec[cc2vid_output[item[1]]]=1.0
			except:
				pass

	tp=0.0
	fp=0.0
	fn=0.0
	for i in range(0,len(prediction)):
		if body_vec[i]:
			if prediction[i]>threshold:
				tp+=1.0
			else:
				fn+=1.0
		else:
			if prediction[i]>threshold:
				fp+=1.0

	try:
		P=tp/(tp+fp)
	except:
		P=0.0
	try:
		R=tp/(tp+fn)
	except:
		R=0.0
	try:
		F=2*P*R/(P+R)
	except:
		F=0.0
	return P,R,F


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
		bownn_model.load_model(load_path)
		abs_vec,prediction=get_prediction(bownn_model,abs_path,in_dict)
	else:
		author_path=opt.author
		author_dict=util.load_sups(author_path)
		authors_path=opt.authors
		bownn_model=BOWNN_author()
		bownn_model.load_model(load_path)
		abs_vec,prediction=get_prediction_author(bownn_model,abs_path,authors_path,in_dict,author_dict)

	print("Entity mentions in this abstract:")
	print_vec(abs_vec,entity_dict)
	print("\n")
	print("Entity mentions predicted:")
	print_vec(prediction,entity_dict,threshold)
	print("\n")

	if evaluate:
		body_path=opt.body
		P,R,F=eval_prediction(prediction,body_path,out_dict,threshold)
		print("Threshold: %.3f, Precision: %.3f, Recall: %.3f, F1: %.3f."%(threshold,P,R,F))

if __name__=='__main__':
	main()