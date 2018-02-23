from scipy.sparse import lil_matrix, csc_matrix, save_npz, load_npz

KG=load_npz("/home/ubuntu/results/ontology/KG_raw.npz")

Jaccard=lil_matrix((133610,133610))
common_neighbor=lil_matrix((133610,133610))

for i in range(0,133610):
    for j in range(i,133610):
        if i==j:
            jacc=1.0
            Jaccard[i,i]=jacc
        else:
            u=KG.getrow(i)
            v=KG.getrow(j)
            set_u=set(u.nonzero()[1])
            set_v=set(u.nonzero()[1])
            comm=float(len(set_u&set_v))
            jacc=float(len(set_u&set_v))/float(len(set_u|set_v))
            Jaccard[i,j]=jacc
            Jaccard[j,i]=jacc
            common_neighbor[i,j]=comm
            common_neighbor[j,i]=comm

save_npz("/home/ubuntu/results/ontology/Jaccard.npz",Jaccard.tocsc())