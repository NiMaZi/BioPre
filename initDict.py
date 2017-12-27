import csv

entity_dict_list=[]

entity_dict={}
entity_dict_abs={}
entity_dict_body={}

for i in range(0,10):
	entity_dict={}
	entity_dict_abs={}
	entity_dict_body={}

	with open("/home/ubuntu/thesiswork/data/abs"+str(i)+".txt.mentions","r",newline='') as csvfile:
		reader = csv.reader(csvfile)
		for item in reader:
			if item[2]=="ConceptName":
				continue
			if item[2] in entity_dict_abs:
				entity_dict_abs[item[2]]=entity_dict_abs[item[2]]+1
			else:
				entity_dict_abs[item[2]]=1

	with open("/home/ubuntu/thesiswork/data/body"+str(0)+".txt.mentions","r",newline='') as csvfile:
		reader = csv.reader(csvfile)
		for item in reader:
			if item[2]=="ConceptName":
				continue
			if item[2] in entity_dict_body:
				entity_dict_body[item[2]]=entity_dict_body[item[2]]+1
			else:
				entity_dict_body[item[2]]=1

	entity_dict["abs"]=entity_dict_abs
	entity_dict["body"]=entity_dict_body

	entity_dict_list.append(entity_dict)

print(entity_dict_list)