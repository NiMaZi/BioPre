import sys
import csv
import pickle

volume=int(sys.argv[1])

tf=[]
idf=[]
word_list=set([])

for i in range(0,volume):
	tmp_tf={}
	with open("/home/ubuntu/thesiswork/data/abs"+str(i)+".txt.mentions","r",newline='',encoding='utf-8') as csvfile:
		reader=csv.reader(csvfile)
		for item in reader:
			if item[2]=="ConceptName":
				continue
			word_list.add(item[2])
			if item[2] in tmp_tf:
				tmp_tf[item[2]]+=1
			else:
				tmp_tf[item[2]]=1
	with open("/home/ubuntu/thesiswork/data/body"+str(i)+".txt.mentions","r",newline='',encoding='utf-8') as csvfile:
		reader=csv.reader(csvfile)
		for item in reader:
			if item[2]=="ConceptName":
				continue
			word_list.add(item[2])
			if item[2] in tmp_tf:
				tmp_tf[item[2]]+=1
			else:
				tmp_tf[item[2]]=1
	tf.append(tmp_tf)

for i in range(0,len(tf)):
	print(tf[i])
print(word_list)