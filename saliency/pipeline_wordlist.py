import csv
import json

word_list=set()
word_dict={}

f=open("/home/ubuntu/NCIT.csv",'r',encoding='utf-8')
reader=csv.reader(f)
count=0
for item in reader:
	if item[0]=="Class ID":
		continue
	CID=item[38]
	entity=item[1]
	s_type=item[188].split('|')
	word_list.add(CID)
	word_dict[CID]={"entity_name":entity,"semantic_type":s_type}
	count+=1
	if count>=10:
		break
f.close()

f=open("/home/ubuntu/results_new/ontology/word_list.json","w")
s=json.dumps(word_list)
f.write(s)
f.close()

f=open("/home/ubuntu/results_new/ontology/word_dict.json","w")
s=json.dumps(word_dict)
f.write(s)
f.close()