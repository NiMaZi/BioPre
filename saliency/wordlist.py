# after distanced

import pickle
import numpy as np

f=open("/home/ubuntu/results/saliency/distanced.pkl","rb")
dis_list=pickle.load(f)
f.close()

word_set=set()
listed_word_set=[]

for entry in dis_list:

	entry_set=set()

	_list=entry['abs']
	for item in _list:
		entry_set.add(item[1])
		word_set.add(item[1])

	_list=entry['body']
	for item in _list:
		entry_set.add(item[1])
		word_set.add(item[1])

	_list=entry['title']
	for item in _list:
		entry_set.add(item[1])
		word_set.add(item[1])

	_list=entry['keywords']
	for item in _list:
		entry_set.add(item[1])
		word_set.add(item[1])

	listed_word_set.append(entry_set)

word_list=list(word_set)

print(len(word_list))

f=open("/home/ubuntu/results/saliency/wordlist.pkl","wb")
pickle.dump(word_list,f)
f.close()

idf=[]
volume=len(dis_list)

for word in word_list:
	d_count=0
	for doc in listed_word_set:
		if word in doc:
			d_count+=1
	idf.append(np.log(float(volume)/float(d_count)))

f=open("/home/ubuntu/results/saliency/idf.pkl","wb")
pickle.dump(idf,f)
f.close()