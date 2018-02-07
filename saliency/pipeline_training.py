# import csv
import sys
# import json
# import math
# import random
# import numpy as np
# from sklearn import svm
# from difflib import SequenceMatcher as Sqm

from semantic_type import isolated_num
from semantic_type import isolated_list

volume=int(sys.argv[1])
samples=[]

for i in range(0,volume):
	f=open("/home/ubuntu/thesiswork/kdata/abs"+str(i)+".txt",'r')
	doc=f.read()
	abs_length=len(doc)
	f.close()
	abs_dict={}
	print(isolated_num)
	f=open("/home/ubuntu/thesiswork/kdata/abs"+str(i)+".csv",'r',encoding='utf-8')
