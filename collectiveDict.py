import pickle

article_dict_list=[]
entity_dict={}

f=open("/home/ubuntu/results/initDict.pickle","rb")
article_dict_list=pickle.load(f)
f.close()

count=0

for entry in article_dict_list:
	e_abs=entry['abs']
	e_body=entry['body']
	if not e_abs:
		continue
	for key in e_abs.keys():
		n_body={k:float(e_body[k]/e_abs[key]) for k in e_body.keys()}
		if key in entity_dict:
			entity_dict[key][0]=entity_dict[key][0]+1.0
			oDict=entity_dict[key][1]
			_tmp={k:oDict.get(k,0.0)+n_body.get(k,0.0) for k in set(oDict.keys()) | set(n_body.keys())}
			entity_dict[key][1]=_tmp
		else:
			entity_dict[key]=[1.0,n_body]
	count=count+1
	if count>5:
		break

for key in entity_dict.keys():
	oDict=entity_dict[key][1]
	_tmp={k:float(oDict[k]/entity_dict[key][0]) for k in oDict.keys()}
	entity_dict[key]=_tmp
	print(key)
	print(entity_dict[key])
	print("\n")

