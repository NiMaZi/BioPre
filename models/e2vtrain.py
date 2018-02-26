import json
from gensim.models import word2vec

# sentences=word2vec.LineSentence("/home/ubuntu/thesiswork/source/corpus/corpus5000.txt")
sentences=word2vec.LineSentence("/home/ubuntu/results/hivo_corpus.txt")

f=open("/home/ubuntu/results/statistics/tf_all.json",'r')
tf_all=json.load(f)
f.close()

tf_all_com={}
for k in tf_all.keys():
	tf_all_com[k]=tf_all[k]+1e-10

model=word2vec.Word2Vec(sg=0,size=200,window=10,min_count=0,sample=1e-3,hs=0,negative=1,sorted_vocab=1)
model.build_vocab_from_freq(tf_all_com)
model.train(sentences,total_examples=9324,epochs=100)
# path="/home/ubuntu/results/models/e2v_sg_5000_e100.model"
path="/home/ubuntu/results/e2v_sg_e100.model"
model.save(path)

model=word2vec.Word2Vec(sg=1,size=200,window=10,min_count=0,sample=1e-3,hs=0,negative=1,sorted_vocab=1)
model.build_vocab_from_freq(tf_all_com)
model.train(sentences,total_examples=9324,epochs=100)
# path="/home/ubuntu/results/models/e2v_cbow_5000_e100.model"
path="/home/ubuntu/results/e2v_cbow_e100.model"
model.save(path)