import sys
import csv
import json
from scipy.sparse import lil_matrix

f=open("/home/ubuntu/results_new/ontology/wordlist_id.json",'r',encoding='utf-8')
wlid=json.load(f)
f.close()

dev_mat=lil_matrix((len(wlid),len(wlid)))

print(type(dev_mat))