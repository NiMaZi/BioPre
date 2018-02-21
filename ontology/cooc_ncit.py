import sys
import csv
import json
import time
from scipy.sparse import lil_matrix, csc_matrix, save_npz, load_npz

f=open("/home/ubuntu/results_new/ontology/wordlist_id.json",'r',encoding='utf-8')
wlid=json.load(f)
f.close()

dev_mat=lil_matrix((len(wlid),len(wlid)))

volume=int(sys.argv[1])
avg_time=0.0

for i in range(0,volume):
	mention_set=set()
	check_point_1=time.time()
	with open("/home/ubuntu/thesiswork/kdata/abs"+str(i)+".csv","r",encoding='utf-8') as csvfile:
		reader=csv.reader(csvfile)
		for item in reader:
			if item[2]=="ConceptName":
				continue
			mention_set.add("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#"+item[1])
	with open("/home/ubuntu/thesiswork/kdata/body"+str(i)+".csv","r",encoding='utf-8') as csvfile:
		reader=csv.reader(csvfile)
		for item in reader:
			if item[2]=="ConceptName":
				continue
			mention_set.add("http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#"+item[1])
	mention_list=list(mention_set)
	check_point_2=time.time()
	node_list={}
	for j1 in range(0,len(mention_list)):
		for j2 in range(j1,len(mention_list)):
			mention1=mention_list[j1]
			mention2=mention_list[j2]
			if mention1==mention2:
				continue
			m_index1=wlid.index(mention1)
			m_index2=wlid.index(mention2)
			if (m_index1,m_index2) in node_list.keys():
				node_list[(m_index1,m_index2)]+=1.0
				node_list[(m_index2,m_index1)]+=1.0
			else:
				node_list[(m_index1,m_index2)]=1.0
				node_list[(m_index2,m_index1)]=1.0
	check_point_3=time.time()
	for (m,n) in node_list.keys():
		dev_mat[m,n]+=node_list[(m,n)]/float(volume)
	check_point_4=time.time()
	print(check_point_2-check_point_1,check_point_3-check_point_2,check_point_4-check_point_3)
	avg_time+=check_point_4-check_point_1
avg_time/=volume
print(avg_time)