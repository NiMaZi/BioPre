import json
import numpy as np
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Reshape, Bidirectional
from keras.callbacks import EarlyStopping
from gensim.models import word2vec as w2v

def load_models():
    path="/home/ubuntu/results/models/e2v_sg_5000_e100.model"
    e2v_model=w2v.Word2Vec.load(path)
    f=open("/home/ubuntu/results/ontology/KG_n2v.json",'r')
    n2v_model=json.load(f)
    f.close()
    return e2v_model,n2v_model

e2v_model,n2v_model=load_models()

def load_sups():
    f=open("/home/ubuntu/results/ontology/c2id.json",'r')
    c2id=json.load(f)
    f.close()
    prefix='http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#'
    return c2id,prefix

c2id,prefix=load_sups()

def get_emb(_code):
    e_vec=list(e2v_model.wv[_code])
    n_vec=n2v_model[str(c2id[prefix+_code])]
    return e_vec+n_vec

def load_corpus(_path):
    f=open(_path,'r')
    pre_corpus=f.read()
    f.close()
    pre_list=pre_corpus.split("\n")[:-1]
    corpus=[]
    m_len=0
    for p in pre_list:
        _p=p.split(" ")[:-1]
        if len(_p)>m_len:
            m_len=len(_p)
        corpus.append(_p)
    return corpus,m_len

path="/home/ubuntu/thesiswork/source/corpus/fullcorpus100.txt"
corpus,maxlen=load_corpus(path)

def build_model(_input_dim,_input_length):
    model=Sequential()
    model.add(LSTM(_input_dim,input_dim=_input_dim,input_length=_input_length,return_sequences=True,activation="linear"))
    model.add(Reshape((_input_length*_input_dim,), input_shape=(_input_length,_input_dim)))
    model.add(Dense(int(_input_dim*_input_length*1.5),input_dim=_input_dim*_input_length,activation="sigmoid"))
    model.add(Dense(_input_dim*_input_length,input_dim=int(_input_dim*_input_length*1.5),activation="linear"))
    model.add(Reshape((_input_length,_input_dim), input_shape=(_input_dim*_input_length,)))
    model.add(Bidirectional(LSTM(_input_dim,input_dim=_input_dim,input_length=_input_length,return_sequences=False,activation="relu"),merge_mode='ave'))
    model.compile(optimizer='rmsprop',loss='binary_crossentropy')
    return model

def build_data(_corpus,_maxlen):
    ndata=[]
    i=0
    comp_vec=[0.0 for i in range(0,400)]
    while(i<5):
    # while(i<len(_corpus)-1):
        _abs=_corpus[i]
        a_emb=[]
        for w in _abs:
            a_emb.append(get_emb(w))
        for j in range(len(a_emb),_maxlen):
            a_emb.append(comp_vec)
        i+=1
        _body=_corpus[i]
        for w in _body:
            ndata.append(a_emb+[get_emb(w)])
    print("pre-processed.")
    N_all=np.array(ndata)
    X_train=N_all[:,:-1,:]
    y_train=N_all[:,-1,:]
    input_dim=X_train.shape[2]
    input_length=X_train.shape[1]
    return X_train,y_train,input_dim,input_length

X_train,y_train,input_dim,input_length=build_data(corpus,maxlen)

print("got data.")
model=build_model(input_dim,input_length)

print("model built.")
print(input_dim,input_length)