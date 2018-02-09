import csv
import sys
import pickle
import numpy as np

prelist=[]
word_list=[]
id2name={}

with open("/Users/yalunzheng/Downloads/NCIT.csv","r",newline='',encoding='utf-8') as csvfile:
	reader=csv.reader(csvfile)
	count=0.0
	c_count=[0.0 for i in range(0,209)]
	c_types=['none' for i in range(0,209)]
	semantic_types=set()
	cids=[]
	for item in reader:
		if item[38]=="C50362":
			print(item)
			sys.exit(0)
		if item[0]=="Class ID":
			c_names=item
			continue
		# if item[7]==item[0]:
		# 	print(item)
		# 	break
		# semantic_types.add(item[188])
		# cids.append(int(item[38].split('C')[1]))
		for c in range (0,len(item)):
			if str(item[c]):
				c_types[c]=item[c]
				c_count[c]+=1
			# print(c_name,item.index(c_name))
		count+=1
	# print(count)
	# print(len(semantic_types))
	# print(semantic_types)

	# scids=sorted(cids)
	# print(len(scids))
	# print(scids[0]) 191
	# for i in range(0,133609):
		# if not scids[i]==(i+191):
			# print(i,scids[i])

	# debined=set()
	# for st in semantic_types:
	# 	dst=st.split('|')
	# 	for d in dst:
	# 		debined.add(d)

	# print(len(debined))
	# print(debined)
	ff=open("/Users/yalunzheng/Downloads/NCITsample.csv",'w',encoding='utf-8')
	wr=csv.writer(ff)
	for n in range(0,len(c_names)):
		if c_count[n]:
			print(n,c_names[n],c_count[n],c_count[n]/count,c_types[n])
			wr.writerow([n,c_names[n],c_count[n],c_count[n]/count,c_types[n]])
	ff.close()
		# if count>0:
			# break
		# if item[0]=='Class ID':
		# 	continue
		# id2name[item[0]]=item[1]
		# word_list.append(item[1])
		# prelist.append([item[0],item[1],item[7]])

# ontology_dmat=np.zeros((len(prelist),len(prelist))) # directed
# ontology_nmat=np.zeros((len(prelist),len(prelist))) # non-directed

# miss_count=0
# root=0
# for i in range(0,len(prelist)):
# 	if not prelist[i][2]:
# 		root=i
# 		continue
# 	_list=prelist[i][2].split('|')
# 	for item in _list:
# 		ontology_dmat[word_list.index(id2name[item])][word_list.index(prelist[i][1])]=1
# 		ontology_nmat[word_list.index(id2name[item])][word_list.index(prelist[i][1])]=1
# 		ontology_nmat[word_list.index(prelist[i][1])][word_list.index(id2name[item])]=1

# print(root)

# 	ontology_dmat[word_list.index(id2name[item[2]])][word_list.index(item[1])]=1
# 	ontology_nmat[word_list.index(id2name[item[2]])][word_list.index(item[1])]=1
# 	ontology_nmat[word_list.index(item[1])][word_list.index(id2name[item[2]])]=1

# for i in range(0,len(prelist)):
# 	if ontology_dmat[79][i]==1:
# 		print(word_list[i])

# dist=np.zeros((len(prelist),len(prelist)))

# for i in range(0,len(prelist)):
# 	for j in range(0,len(prelist)):
# 		dist[i][j]=np.inf

# for i in range(0,len(prelist)):
# 	dist[i][i]=0.0

# for i in range(0,len(prelist)):
# 	for j in range(0,len(prelist)):
# 		if ontology_nmat[i][j]==1:
# 			dist[i][j]=1

# for k in range(0,len(prelist)):
# 	for i in range(0,len(prelist)):
# 		for j in range(0,len(prelist)):
# 			if dist[i][j]>(dist[i][k]+dist[k][j]):
# 				dist[i][j]=dist[i][k]+dist[k][j]

# f=open("/Users/yalunzheng/Documents/BioPre/ontology_wordlist.pkl","wb")
# pickle.dump(word_list,f)
# f.close()

# f=open("/Users/yalunzheng/Documents/BioPre/ontology_tree.pkl","wb")
# pickle.dump(ontology_dmat,f)
# f.close()

# f=open("/Users/yalunzheng/Documents/BioPre/ontology_map.pkl","wb")
# pickle.dump(ontology_nmat,f)
# f.close()

# f=open("/Users/yalunzheng/Documents/BioPre/ontology_path.pkl","wb")
# pickle.dump(dist,f)
# f.close()