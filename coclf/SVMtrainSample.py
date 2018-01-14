import sys
import pickle

split_ratio=float(sys.argv[1])

f=open("/home/ubuntu/results/saliency/featured.pkl","rb")
featured_list=pickle.load(f)
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

for entry in featured_list:
	abs_dict=entry['abs']
	body_dict=entry['body']
	for a_key in abs_dict.keys():
		for b_key in body_dict.keys():
			sample_prelist.append([a_key,b_key,abs_dict[a_key][0],abs_dict[a_key][1]-abs_dict[a_key][0],abs_dict[a_key][2]],body_dict[a_key][0],body_dict[a_key][1]-body_dict[a_key][0],body_dict[a_key][2]])

for i in range(0,10):
	print(sample_prelist[i])

print(len(sample_prelist))