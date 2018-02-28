import json
import numpy as np
from keras.models import Sequential, load_model
from keras.layers import LSTM, Bidirectional, Masking
from keras.callbacks import EarlyStopping
from gensim.models import word2vec as w2v

dim=128
maxlen=290

def load_models():
    path="/home/ubuntu/results/models/e2v_sg_10000_e100_d64.model"
    e2v_model=w2v.Word2Vec.load(path)
    f=open("/home/ubuntu/results/ontology/KG_n2v_d64.json",'r')
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
    for i,p in enumerate(pre_list):
        _p=p.split(" ")[:-1]
        corpus.append(_p)
    return corpus

path="/home/ubuntu/thesiswork/source/corpus/fullcorpus100.txt"
corpus=load_corpus(path)

def build_model(_input_dim,_input_length):
    model=Sequential()
    model.add(Masking(mask_value=0.0,input_shape=(_input_length,_input_dim)))
    model.add(Bidirectional(LSTM(_input_dim,return_sequences=False,activation="tanh"),merge_mode='ave'))
    model.compile(optimizer='adam',loss='binary_crossentropy')
    return model

model=build_model(dim,maxlen)

def train_on_data(_corpus,_maxlen,_model,_epochs):
    early_stopping=EarlyStopping(monitor='loss',patience=10)
    i=0
    comp_vec=[0.0 for i in range(0,128)]
    while(i<len(_corpus)-1):
        print("training on doc "+str(i))
        ndata=[]
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
        N_all=np.array(ndata)
        X_train=N_all[:,:-1,:]
        y_train=N_all[:,-1,:]
        _model.fit(X_train,y_train,batch_size=128,epochs=_epochs,verbose=0,callbacks=[early_stopping])
    _model.save("/home/ubuntu/results/models/LSTM100.h5")

train_on_data(corpus,maxlen,model,50)