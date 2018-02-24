from gensim.models import word2vec

sentences=word2vec.LineSentence("/home/ubuntu/thesiswork/source/corpus/corpus5000.txt")

f=open("/home/ubuntu/results/statistics/tf_all.json",'r')
tf_all=json.load(f)
f.close()
tf_all_com={}
for k in tf_all.keys():
    tf_all_com[k]=tf_all[k]+1e-5

model=word2vec.Word2Vec(sentences,sg=0,size=200,window=10,min_count=0,sample=1e-3,hs=0,negative=1,sorted_vocab=1)
path="/home/ubuntu/results/models/e2v_sg_5000.model"
model.save(path)

model=word2vec.Word2Vec(sentences,sg=1,size=200,window=10,min_count=0,sample=1e-3,hs=0,negative=1,sorted_vocab=1)
path="/home/ubuntu/results/models/e2v_cbow_5000.model"
model.save(path)