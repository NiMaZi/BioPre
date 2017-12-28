import sys
import csv
import pickle

freq_threshold=float(sys.argv[1])
test_volume=int(sys.argv[2])
entity_dict={}

f=open("/home/ubuntu/results/collectiveDict.pickle","rb")
entity_dict=pickle.load(f)
f.close()

total_hit_rate=0.0
total_error_rate=0.0

for i in range(2000,2000+test_volume):
	prediction=set([])
	mention=set([])
	with open("/home/ubuntu/thesiswork/data/abs"+str(i)+".txt.mentions","r",newline='') as csvfile:
		reader=csv.reader(csvfile)
		for item in reader:
			if item[2]=="ConceptName":
				continue
			if item[2] in entity_dict:
				for key in entity_dict[item[2]].keys():
					if entity_dict[item[2]][key]>freq_threshold:
						prediction.add(key)
	with open("/home/ubuntu/thesiswork/data/body"+str(i)+".txt.mentions","r",newline='') as csvfile:
		reader=csv.reader(csvfile)
		for item in reader:
			if item[2]=="ConceptName":
				continue
			if item[2] not in mention:
				mention.add(item[2])
	hit_rate=float(len(prediction&mention))/float(len(mention))
	error_rate=1-float(len(prediction&mention))/float(len(prediction))
	total_hit_rate=total_hit_rate+hit_rate
	total_error_rate=total_error_rate+error_rate
	print("hit rate in article "+str(i)+": "+str(hit_rate)+".\n")
	print("error rate in article "+str(i)+": "+str(error_rate)+".\n")
print("total hit rate: "+str(total_hit_rate)+".\n")
print("total error rate: "+str(total_error_rate)+".\n")