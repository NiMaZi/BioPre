import csv
import pickle
import numpy as np

prelist=[]
word_list=[]
id2name={}

with open("/Users/yalunzheng/Documents/BioPre/HIVO004.csv","r",newline='',encoding='utf-8') as csvfile:
	reader=csv.reader(csvfile)
	for item in reader:
		if item[0]=='Class ID':
			continue
		id2name[item[0]]=item[1]
		word_list.append(item[1])
		prelist.append([item[0],item[1],item[7]])

ontology_dmat=np.zeros((len(prelist),len(prelist))) # directed
ontology_nmat=np.zeros((len(prelist),len(prelist))) # non-directed

# miss_count=0
root=0
for i in range(0,len(prelist)):
	if not prelist[i][2]:
		root=i
		continue
	_list=prelist[i][2].split('|')
	for item in _list:
		ontology_dmat[word_list.index(id2name[item])][word_list.index(prelist[i][1])]=1
		ontology_nmat[word_list.index(id2name[item])][word_list.index(prelist[i][1])]=1
		ontology_nmat[word_list.index(prelist[i][1])][word_list.index(id2name[item])]=1

print(root)

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

f=open("/Users/yalunzheng/Documents/BioPre/ontology_tree.pkl","wb")
pickle.dump(ontology_dmat,f)
f.close()

f=open("/Users/yalunzheng/Documents/BioPre/ontology_map.pkl","wb")
pickle.dump(ontology_nmat,f)
f.close()

# f=open("/Users/yalunzheng/Documents/BioPre/ontology_path.pkl","wb")
# pickle.dump(dist,f)
# f.close()