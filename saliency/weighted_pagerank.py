import sys
import pickle
import numpy as np

mode=int(sys.argv[1])
threshold=float(sys.argv[2])

f=open("/home/ubuntu/results/saliency/wordlist.pkl","rb")
word_list=pickle.load(f)
f.close()

if mode==1:
	f=open("/home/ubuntu/results/saliency/simplemat.pkl","rb")
	dev_mat=pickle.load(f)
	f.close()
else:
	sys.exit(0)

VR=[float(1.0/(len(word_list))) for i in range(0,len(word_list))]
NVR=[float(1.0/(len(word_list))) for i in range(0,len(word_list))]

epoch=0
d=0.85

while True:
	for i in range(0,len(VR)):
		inw=0.0
		for j in range(0,len(VR)):
			outw=0.0
			for k in range(0,len(VR)):
				outw+=dev_mat[j][k]
			inw+=(dev_mat[j][i]/outw)*VR[j]
		NVR[i]=(1.0-d)+d*inw
	delta=0.0
	for i in range(0,len(VR)):
		delta+=abs(NVR[i]-VR[i])
	epoch+=1
	for i in range(0,len(VR)):
		VR[i]=NVR[i]
	if delta<threshold:
		break

print(epoch)
