import sys
import csv
import pickle
import numpy as np

volume=int(sys.argv[1])

tf=[]
tf_word=[]
idf=[]
word_list=set([])

for i in range(0,volume):
	tmp_tf={}
	word_count=0
	with open("/home/ubuntu/thesiswork/data/abs"+str(i)+".txt.mentions","r",newline='',encoding='utf-8') as csvfile:
		reader=csv.reader(csvfile)
		for item in reader:
			if item[2]=="ConceptName":
				continue
			word_count+=1
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
			word_count+=1
			word_list.add(item[2])
			if item[2] in tmp_tf:
				tmp_tf[item[2]]+=1
			else:
				tmp_tf[item[2]]=1
	tf.append([tmp_tf,word_count])

sorted_word_list=sorted(word_list)

for word in sorted_word_list:
	_tmp=[]
	d_count=0
	for i in range(0,volume):
		if word in tf[i][0]:
			freq=float(tf[i][0][word])/float(tf[i][1])
			d_count+=1
		else:
			freq=0.0
		_tmp.append(freq)
	tf_word.append(_tmp)
	idf.append(np.log(float(volume)/float(d_count)))


print(sorted_word_list)

for row in tf_word:
	print(row)

print(idf)