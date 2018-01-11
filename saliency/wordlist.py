# after distanced

import pickle

f=open("/home/ubuntu/results/saliency/distanced.pkl","rb")
dis_list=pickle.load(f)
f.close()

word_set=set()

for entry in dis_list:

	_list=entry['abs']
	for item in _list:
		word_set.add(item[1])

	_list=entry['body']
	for item in _list:
		word_set.add(item[1])

	_list=entry['title']
	for item in _list:
		word_set.add(item[1])

	_list=entry['keywords']
	for item in _list:
		word_set.add(item[1])

word_list=list(word_set)

f=open("/home/ubuntu/results/saliency/wordlist.pkl","wb")
pickle.dump(word_list,f)
f.close()