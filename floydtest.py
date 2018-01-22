import pickle
import numpy as np

f=open("/Users/yalunzheng/Documents/BioPre/ontology_wordlist.pkl","rb")
word_list=pickle.load(f)
f.close()

f=open("/Users/yalunzheng/Documents/BioPre/ontology_tree.pkl","rb")
tmat=pickle.load(f)
f.close()

dist=[[np.inf for i in range(0,len(word_list))] for i in range(0,len(word_list))]
path=[[-1 for i in range(0,len(word_list))] for i in range(0,len(word_list))]
path_list=[[[] for i in range(0,len(word_list))] for i in range(0,len(word_list))]

def floyd(mat,path):
	for i in range(0,len(mat)):
		for j in range(0,len(mat)):
			for k in range(0,len(mat)):
				print(i,j,k)
				if mat[i][j]>mat[i][k]+mat[k][j]:
					mat[i][j]=mat[i][k]+mat[k][j]
					path[i][j]=k

def get_path(i,j,path):
	if path[i][j]==-1:
		return []
	else:
		path_list=get_path(i,path[i][j],path)
		path_list.append(path[i][j])
		path_list.extend(get_path(path[i][j],j,path))
		return path_list


floyd(dist,path)

for i in range(0,4):
	for j in range(0,4):
		if i==j:
			continue
		print(i,j,mat[i][j])
		p_list=[i]
		p_list.extend(get_path(i,j,path))
		p_list.append(j)
		path_list[i][j].extend(p_list)
		print(path_list[i][j])
		

f=open("/Users/yalunzheng/Documents/BioPre/ontology_dist.pkl","wb")
pickle.dump(dist,f)
f.close()

f=open("/Users/yalunzheng/Documents/BioPre/ontology_path.pkl","wb")
pickle.dump(path_list,f)
f.close()