import sys
import csv
import json
from scipy.sparse import lil_matrix

f=open("/home/ubuntu/results_new/ontology/wordlist_id.json",'r',encoding='utf-8')
wlid=json.load(f)
f.close()

dev_mat=lil_matrix((len(wlid)-1,len(wlid)-1))

volume=int(sys.argv[1])

for i in range(0,volume):
	mention_set=set()
	with open("/home/ubuntu/thesiswork/kdata/abs"+str(i)+".csv","r",encoding='utf-8') as csvfile:
		reader=csv.reader(csvfile)
		for item in reader:
			if item[2]=="ConceptName":
				continue
			mention_set.add(item[1])
	with open("/home/ubuntu/thesiswork/kdata/body"+str(i)+".csv","r",encoding='utf-8') as csvfile:
		reader=csv.reader(csvfile)
		for item in reader:
			if item[2]=="ConceptName":
				continue
			mention_set.add(item[1])
	print(mention_set)