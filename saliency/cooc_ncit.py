# import sys
# import csv
import json
# from scipy.sparse import lil_matrix

f=open("/home/ubuntu/results_new/ontology/wordlist_id.json",'r',encoding='utf-8')
wlid=json.load(f)
f.close()

f=open("/home/ubuntu/results_new/ontology/word_list.json",'r',encoding='utf-8')
wl=json.load(f)
f.close()

for i in range(0,len(wl)):
	if not wl[i]==wlid[i+1].split('#')[1]:
		print(wl[i],wlid[i+1])