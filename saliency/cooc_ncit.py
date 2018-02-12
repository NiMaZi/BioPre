import sys
import csv
import json
from scipy.sparse import lil_matrix

f=open("/home/ubuntu/results_new/ontology/wordlist_id.json",'r',encoding='utf-8')
wlid=json.load(f)
f.close()

dev_mat=lil_matrix((len(wlid),len(wlid)))

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
	for j1 in range(0,len(mention_set)):
		for j2 in range(j1,len(mention_set)):
			mention1=list(mention_set)[j1]
			mention2=list(mention_set)[j2]
			if mention1==mention2:
				continue
			print(mention1,mention2)
			m_index1=wlid.index("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#"+mention1)
			m_index2=wlid.index("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#"+mention2)
			if m_index1<m_index2:
				dev_mat[m_index1,m_index2]+=1.0/float(volume)
			else:
				dev_mat[m_index2,m_index1]+=1.0/float(volume)