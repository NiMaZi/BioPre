import csv
import json

volume=1200

word_set=set()
for i in range(0,volume):
	f=open("/home/ubuntu/thesiswork/kdata/abs"+str(i)+".csv",'r',encoding='utf-8')
	rd=csv.reader(f)
	for item in rd:
		if item[1]=="ConceptCode":
			continue
		word_set.add(item[1])
	f.close()

	f=open("/home/ubuntu/thesiswork/kdata/body"+str(i)+".csv",'r',encoding='utf-8')
	rd=csv.reader(f)
	for item in rd:
		if item[1]=="ConceptCode":
			continue
		word_set.add(item[1])
	f.close()

	f=open("/home/ubuntu/thesiswork/kdata/title"+str(i)+".csv",'r',encoding='utf-8')
	rd=csv.reader(f)
	for item in rd:
		if item[1]=="ConceptCode":
			continue
		word_set.add(item[1])
	f.close()

	f=open("/home/ubuntu/thesiswork/kdata/keywords"+str(i)+".csv",'r',encoding='utf-8')
	rd=csv.reader(f)
	for item in rd:
		if item[1]=="ConceptCode":
			continue
		word_set.add(item[1])
	f.close()

# print(word_set)
print(len(word_set))