import csv
import sys
import math
import random
import numpy as np
from sklearn import svm
from difflib import SequenceMatcher as Sqm

volume=int(sys.argv[1])
samples=[]

for i in range(0,500):
	f=open("/home/ubuntu/thesiswork/kdata/abs"+str(i)+".txt",'r')
	doc=f.read()
	abs_length=len(doc)
	f.close()
	abs_dict={}
	f=open("/home/ubuntu/thesiswork/kdata/abs"+str(i)+".csv",'r',encoding='utf-8')
	