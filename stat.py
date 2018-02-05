import sys
import csv
import pickle
from difflib import SequenceMatcher as Sqm

volume=int(sys.argv[1])
real_volume=volume

f=open("/home/ubuntu/results/saliency/keywords_list","rb")
keywords_list=pickle.load(f)
f.close()

record_abs=0.0
record_body=0.0
record_title=0.0
record_kw=0.0
record_sal=0.0
record_cover=0.0

for i in range(0,volume):
	print("counting on article "+str(i)+".")
	record_list_abs=[]
	try:
		with open("/home/ubuntu/thesiswork/kdata/abs"+str(i)+".txt.mentions","r",newline='',encoding='utf-8') as csvfile:
			reader=csv.reader(csvfile)
			for item in reader:
				if item[2]=="ConceptName":
					continue
				mention=item[0]
				entity=item[2]
				record_list_abs.append([mention,entity])
				record_abs+=1
	except:
		real_volume-=1
		continue
	record_list_body=[]
	try:
		with open("/home/ubuntu/thesiswork/kdata/body"+str(i)+".txt.mentions","r",newline='',encoding='utf-8') as csvfile:
			reader=csv.reader(csvfile)
			for item in reader:
				if item[2]=="ConceptName":
					continue
				mention=item[0]
				entity=item[2]
				record_list_body.append(entity)
				record_body+=1
	except:
		real_volume-=1
		continue
	record_list_title=[]
	try:
		with open("/home/ubuntu/thesiswork/kdata/title"+str(i)+".txt.mentions","r",newline='',encoding='utf-8') as csvfile:
			reader=csv.reader(csvfile)
			for item in reader:
				if item[2]=="ConceptName":
					continue
				mention=item[0]
				entity=item[2]
				record_list_title.append(entity)
				record_title+=1
	except:
		real_volume-=1
		continue
	record_list_kw=[]
	try:
		with open("/home/ubuntu/thesiswork/kdata/keywords"+str(i)+".txt.mentions","r",newline='',encoding='utf-8') as csvfile:
			reader=csv.reader(csvfile)
			for item in reader:
				if item[2]=="ConceptName":
					continue
				mention=item[0]
				entity=item[2]
				record_list_kw.append(entity)
				record_kw+=1
	except:
		real_volume-=1
		continue
	for record in record_list_abs:
		if record[1] in record_list_body:
			record_cover+=1
		if record[1] in record_list_kw or record[1] in record_list_title:
			record_sal+=1
			continue
		for kw in keywords_list[i]:
			if Sqm(None,kw,record[0].lower()).ratio()>=0.5:
				record_sal+=1
				break

record_abs/=real_volume
record_body/=real_volume
record_title/=real_volume
record_kw/=real_volume
record_sal/=real_volume
record_cover/=real_volume

print(record_abs,record_body,record_title,record_kw,record_sal,record_sal/record_abs,record_cover/record_abs)