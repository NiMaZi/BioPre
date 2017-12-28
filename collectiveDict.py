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
	e_body=entry['body']
	for key in e_abs.keys():
		print("entity name in abs:")
		print(key)
		if key in entity_dict:
			print("hit abs mention")
			entity_dict[key][0]=entity_dict[key][0]+e_abs[key]
			for bkey in e_body.keys():
				print("\tentity name in body:")
				print(bkey)
				if bkey in entity_dict[key][1]:
					print("\thit body mention")
					print(key)
					print(entity_dict[key][1])
					entity_dict[key][1][bkey]=entity_dict[key][1][bkey]+e_body[bkey]
					print(key)
					print(entity_dict[key][1])
					print(entity_dict["Protein"])
				else:
					print("\tadd body mention")
					print(key)
					print(entity_dict[key][1])
					entity_dict[key][1][bkey]=e_body[bkey]
					print(key)
					print(entity_dict[key][1])
					print(entity_dict["Protein"])
		else:
			print("add abs mention")
			entity_dict[key]=[e_abs[key],e_body]
	print("\n\n")
	for key in entity_dict.keys():
		print(key)
		print(entity_dict[key])
		print("\n")
	count=count+1
	if count>2:
		break

for key in entity_dict.keys():
	print(key)
	print(entity_dict[key])
	print("\n")

