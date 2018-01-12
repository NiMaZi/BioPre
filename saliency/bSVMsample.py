import sys
import pickle

f=open("/home/ubuntu/results/saliency/featured.pkl","rb")
featured_list=pickle.load(f)
f.close()

f=open("/home/ubuntu/results/saliency/distanced.pkl","rb")
dis_list=pickle.load(f)
f.close()

for i in range(0,)