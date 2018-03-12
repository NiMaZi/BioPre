import os
import json
import numpy as np
from keras.models import Sequential, load_model
from keras.layers import LSTM,Bidirectional,Masking,BatchNormalization
from keras.callbacks import EarlyStopping
from gensim.models import word2vec as w2v

dim=128
maxlen=1024
volume=1000
homedir=os.environ['HOME']

def load_models():
    path=homedir+"/results/models/e2v_sg_10000_e100_d64.model"
    e2v_model=w2v.Word2Vec.load(path)
    f=open(homedir+"/results/ontology/KG_n2v_d64.json",'r')
    n2v_model=json.load(f)
    f.close()
    return e2v_model,n2v_model

e2v_model,n2v_model=load_models()

def load_sups():
    f=open(homedir+"/results/ontology/c2id.json",'r')
    c2id=json.load(f)
    f.close()
    f=open(homedir+"/results/ontology/full_word_list.json",'r')
    word_list=json.load(f)
    f.close()
    prefix='http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#'
    return c2id,prefix,word_list[1:]

c2id,prefix,word_list=load_sups()

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
    for i,p in enumerate(pre_list):
        _p=p.split(" ")[:-1]
        corpus.append(_p)
    return corpus[volume:volume+200]

path=homedir+"/thesiswork/corpus/fullcorpusall.txt"
corpus=load_corpus(path)

def test_on_data(_corpus,_maxlen,_model):
    i=0
    comp_vec=[0.0 for i in range(0,128)]
    ndata=[]
    while(i<len(_corpus)-1):
        print("testing on doc "+str(i))
        _body=_corpus[i]
        b_emb=[]
        if len(_body)<_maxlen:
            for w in _body:
                b_emb.append(get_emb(w))
            for j in range(len(b_emb),_maxlen):
                b_emb.append(comp_vec)
            ndata=np.array([b_emb])
            y_out=model.predict(ndata)
        else:
            for j in range(0,len(_body)-_maxlen+1):
                b_emb=[]
                for wj in range(0,_maxlen):
                    w=_body[j+wj]
                    b_emb.append(get_emb(w))
                ndata=[b_emb]
                y_out=model.predict(ndata)
        i+=2
        print(len(y_out[0]),y_out[0])


model=load_model(homedir+"/results/models/BiLSTM0.h5")
test_on_data(corpus,maxlen,model)