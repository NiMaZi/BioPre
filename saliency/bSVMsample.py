import sys
import pickle
import random
import numpy as np

split_ratio=float(sys.argv[1])

f=open("/home/ubuntu/results/saliency/featured.pkl","rb")
featured_list=pickle.load(f)
f.close()

f=open("/home/ubuntu/results/saliency/distanced.pkl","rb")
dis_list=pickle.load(f)
f.close()

f=open("/home/ubuntu/results/saliency/wordlist.pkl","rb")
word_list=pickle.load(f)
f.close()

f=open("/home/ubuntu/results/saliency/idf.pkl","rb")
idf=pickle.load(f)
f.close()

f=open("/home/ubuntu/results/saliency/centrality.pkl","rb")
centrality=pickle.load(f)
f.close()

sample_prelist=[]

for i in range(0,len(dis_list)):
	if not dis_list[i]['title'] and not dis_list[i]['keywords']:
		continue
	label_set=set()
	for item in dis_list[i]['title']:
		label_set.add(item[1])
	for item in dis_list[i]['keywords']:
		label_set.add(item[1])
	for key in featured_list[i]['abs'].keys():
		if key in label_set:
			sample_prelist.append([key,featured_list[i]['abs'][key][0],featured_list[i]['abs'][key][1]-featured_list[i]['abs'][key][0],featured_list[i]['abs'][key][2],idf[word_list.index(key)],centrality[key],1]) #(str)entity, (float)distance, (float)spread, (int)count, (float)idf, (float)centrality, label
		else:
			sample_prelist.append([key,featured_list[i]['abs'][key][0],featured_list[i]['abs'][key][1]-featured_list[i]['abs'][key][0],featured_list[i]['abs'][key][2],idf[word_list.index(key)],centrality[key],0])

print(len(sample_prelist))

for i in range(0,10):
	print(sample_prelist[i])

random.shuffle(sample_prelist)
split=int(split_ratio*len(sample_prelist))

key_phrase=[0 for i in range(0,len(word_list))]

for i in range(0,split):
	key_phrase[word_list.index(sample_prelist[i][0])]+=sample_prelist[i][6]

f=open("/home/ubuntu/results/saliency/keyphrase.pkl","wb")
pickle.dump(key_phrase,f)
f.close()

training_list=[]
for i in range(0,split):
	training_list.append([key_phrase[word_list.index(sample_prelist[i][0])],sample_prelist[i][1],sample_prelist[i][2],sample_prelist[i][3],sample_prelist[i][4],sample_prelist[i][5],sample_prelist[i][6]])

f=open("/home/ubuntu/results/saliency/trainlist.pkl","wb")
pickle.dump(training_list,f)
f.close()

test_list=[]
for i in range(split,len(sample_prelist)):
	test_list.append([key_phrase[word_list.index(sample_prelist[i][0])],sample_prelist[i][1],sample_prelist[i][2],sample_prelist[i][3],sample_prelist[i][4],sample_prelist[i][5],sample_prelist[i][6]])

f=open("/home/ubuntu/results/saliency/testlist.pkl","wb")
pickle.dump(test_list,f)
f.close()