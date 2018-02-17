import pickle

f=open("/home/ubuntu/results/saliency/w_count.pkl","rb")
w=pickle.load(f)
f.close()
f=open("/home/ubuntu/results/saliency/wf_count.pkl","rb")
wf=pickle.load(f)
f.close()
f=open("/home/ubuntu/results/saliency/pwf_count.pkl","rb")
pwf=pickle.load(f)
f.close()
f=open("/home/ubuntu/results/saliency/tpwf_count.pkl","rb")
tpwf=pickle.load(f)
f.close()
f=open("/home/ubuntu/results/saliency/fpwf_count.pkl","rb")
fpwfw=pickle.load(f)
f.close()

sw=list(w.keys())
# sw=sorted(w,key=w.get)
# swf=sorted(wf,key=wf.get)
# spwf=sorted(pwf,key=pwf.get)
# stpwf=sorted(tpwf,key=tpwf.get)
# sfpwf=sorted(fpwf,key=fpwf.get)

estat={}

for k in sw:
	if k in pwf.keys():
		print(k,w[k],wf[k],pwf[k],tpwf[k],fpwf[k])
	else:
		print(k,w[k],wf[k],0.0,0.0,0.0)