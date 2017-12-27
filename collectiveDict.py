import pickle

article_dict_list=[]
entity_dict={}

f=open("/home/ubuntu/results/initDict.pickle","rb")
article_dict_list=pickle.load(f)
f.close()

count=0

for entry in article_dict_list:
	print(entry)
	print("\n\n")
	e_abs=entry['abs']
	for key in e_abs.keys():
		e_body=entry['body']
		if key in entity_dict:
			for bkey in e_body.keys():
				if bkey in entity_dict[key]:
					entity_dict[key][bkey]=entity_dict[key][bkey]+e_body[bkey]
				else:
					entity_dict[key][bkey]=e_body[bkey]
		else:
			entity_dict[key]=e_body
	count=count+1
	if count>5:
		break

print(entity_dict)

