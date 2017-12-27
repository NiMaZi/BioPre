import csv

entity_dict={}

with open("/home/ubuntu/thesiswork/data/abs0.txt.mentions","r",newline='') as csvfile:
	reader = csv.reader(csvfile)
	for item in reader:
		if item[2]=="ConceptName":
			continue
		if item[2] in entity_dict:
			entity_dict[item[2]]=entity_dict[item[2]]+1
		else:
			entity_dict[item[2]]=1

print(sorted(entity_dict.items(),key=lambda x:x[1]))