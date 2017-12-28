import pickle

article_dict_list=[]
entity_dict={}

f=open("/home/ubuntu/results/initDict.pickle","rb")
article_dict_list=pickle.load(f)
f.close()

count=0

for entry in article_dict_list:
	print("abs:\n")
	print(entry['abs'])
	print("\n")
	print("body:\n")
	print(entry['body'])
	print("\n\n")
	e_abs=entry['abs']
	for key in e_abs.keys():
		e_body=entry['body']
		if key in entity_dict:
			entity_dict[key][0]=entity_dict[key][0]+float(e_abs[key]/e_abs[key])
			for bkey in e_body.keys():
				if bkey in entity_dict[key][1]:
					entity_dict[key][1][bkey]=entity_dict[key][1][bkey]+float(e_body[bkey]/e_abs[key])
				else:
					entity_dict[key][1][bkey]=float(e_body[bkey]/e_abs[key])
		else:
			entity_dict[key]=[float(e_abs[key]/e_abs[key]),e_body]
	count=count+1
	if count>2:
		break

for key in entity_dict.keys():
	print(key)
	print(entity_dict[key])
	print("\n")

