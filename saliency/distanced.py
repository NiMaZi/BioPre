import sys
import csv
import pickle

start=int(sys.argv[1])
end=int(sys.argv[2])

distanced_list=[]
dlf=open("/home/ubuntu/results/saliency/distanced.pkl","wb")
pickle.dump(distanced_list,dlf)
dlf.close()

for i in range(start,end):
	
	record={}

	record['abs']=[]
	f=open("/home/ubuntu/thesiswork/kdata/abs"+str(i)+".txt","r",encoding='utf-8')
	doc=f.read()
	length=float(len(doc))
	f.close()
	with open("/home/ubuntu/thesiswork/kdata/abs"+str(i)+".txt.mentions","r",newline='',encoding='utf-8') as csvfile:
		reader=csv.reader(csvfile)
		for item in reader:
			if item[2]=="ConceptName":
				continue
			mention=item[0]
			entity=item[2]
			start_pos=float(item[4])/length
			end_pos=float(item[5])/length
			record['abs'].append([mention,entity,start_pos,end_pos])

	record['body']=[]
	f=open("/home/ubuntu/thesiswork/kdata/body"+str(i)+".txt","r",encoding='utf-8')
	doc=f.read()
	length=float(len(doc))
	f.close()
	with open("/home/ubuntu/thesiswork/kdata/body"+str(i)+".txt.mentions","r",newline='',encoding='utf-8') as csvfile:
		reader=csv.reader(csvfile)
		for item in reader:
			if item[2]=="ConceptName":
				continue
			mention=item[0]
			entity=item[2]
			start_pos=float(item[4])/length
			end_pos=float(item[5])/length
			record['body'].append([mention,entity,start_pos,end_pos])

	record['title']=[]
	f=open("/home/ubuntu/thesiswork/kdata/title"+str(i)+".txt","r",encoding='utf-8')
	doc=f.read()
	length=float(len(doc))
	f.close()
	with open("/home/ubuntu/thesiswork/kdata/title"+str(i)+".txt.mentions","r",newline='',encoding='utf-8') as csvfile:
		reader=csv.reader(csvfile)
		for item in reader:
			if item[2]=="ConceptName":
				continue
			mention=item[0]
			entity=item[2]
			start_pos=float(item[4])/length
			end_pos=float(item[5])/length
			record['title'].append([mention,entity,start_pos,end_pos])

	record['keywords']=[]
	f=open("/home/ubuntu/thesiswork/kdata/keywords"+str(i)+".txt","r",encoding='utf-8')
	doc=f.read()
	length=float(len(doc))
	f.close()
	with open("/home/ubuntu/thesiswork/kdata/keywords"+str(i)+".txt.mentions","r",newline='',encoding='utf-8') as csvfile:
		reader=csv.reader(csvfile)
		for item in reader:
			if item[2]=="ConceptName":
				continue
			mention=item[0]
			entity=item[2]
			start_pos=float(item[4])/length
			end_pos=float(item[5])/length
			record['keywords'].append([mention,entity,start_pos,end_pos])

	distanced_list.append(record)

print(distanced_list)
