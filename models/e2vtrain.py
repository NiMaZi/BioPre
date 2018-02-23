from gensim.models import word2vec

sentences=word2vec.LineSentence("/home/ubuntu/thesiswork/source/corpus/corpus5000.txt")

model=word2vec.Word2Vec(sentences,sg=0,size=200,window=10,min_count=0,sample=1e-3,hs=0,negative=1,sorted_vocab=1)
path="/home/ubuntu/results/models/e2v_sg_5000.model"
model.save(path)

model=word2vec.Word2Vec(sentences,sg=1,size=200,window=10,min_count=0,sample=1e-3,hs=0,negative=1,sorted_vocab=1)
path="/home/ubuntu/results/models/e2v_cbow_5000.model"
model.save(path)