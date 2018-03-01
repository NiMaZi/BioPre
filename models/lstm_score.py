import json
import numpy as np
from scipy.spatial.distance import cosine
from keras.models import load_model
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
    f=open("/home/ubuntu/results/ontology/full_word_list.json",'r')
    word_list=json.load(f)[1:]
    f.close()
    prefix='http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#'
    return c2id,prefix,word_list

c2id,prefix,word_list=load_sups()

def get_emb(_code):
    e_vec=list(e2v_model.wv[_code])
    n_vec=n2v_model[str(c2id[prefix+_code])]
    return e_vec+n_vec

def load_corpus(_path):
    f=open(_path,'r')
    pre_corpus=f.read()
    f.close()
    pre_list=pre_corpus.split("\n")[100:150]
    corpus=[]
    for i,p in enumerate(pre_list):
        _p=p.split(" ")[:-1]
        corpus.append(_p)
    return corpus

path="/home/ubuntu/thesiswork/source/corpus/fullcorpus5000.txt"
corpus=load_corpus(path)


def find_match(vec,n):
    m_dict={}
    for w in word_list:
        w_vec=np.array(get_emb(w.split('#')[1]))
        dis=cosine(w_vec,vec)
        m_dict[w.split('#')[1]]=dis
    res=sorted(m_dict,key=m_dict.get)
    return set(res[:n])

def test_on_data(_corpus,_maxlen,_model):
    ratio_body2abs=496.27/59.5
    i=0
    comp_vec=[0.0 for i in range(0,128)]
    P_all=0.0
    R_all=0.0
    while(i<len(_corpus)-1):
        ndata=[]
        _abs=_corpus[i]
        a_emb=[]
        for w in _abs:
            a_emb.append(get_emb(w))
        for j in range(len(a_emb),_maxlen):
            a_emb.append(comp_vec)
        i+=1
        _body=set(_corpus[i])
        i+=1
        ndata.append(a_emb)
        N_all=np.array(ndata)
        y_pred=_model.predict(N_all)
        top_n=int(len(set(_abs))*ratio_body2abs)
        match=find_match(y_pred[0],top_n)
        tp=float(len(match&_body))
        fp=len(match-_body)
        fn=len(_body-match)
        P=tp/(tp+fp)
        R=tp/(tp+fn)
        P_all+=P
        R_all+=R
        try:
            F1=2*P*R/(P+R)
        except:
            F1=0.0
    P_all/=(len(_corpus)/2)
    R_all/=(len(_corpus)/2)
    try:
        F1=2*P_all*R_all/(P_all+R_all)
    except:
        F1=0.0
    f=open("/home/ubuntu/results/logs/BiLSTM100.txt",'a')
    f.write("%.3f,%.3f,%.3f\n"%(P_all,R_all,F1))
    f.close()

# model=load_model("/home/ubuntu/results/models/LSTM100198.h5")
# test_on_data(corpus,maxlen,model)
    
rec=2
while(rec<=198):        
    model=load_model("/home/ubuntu/results/models/LSTM100"+str(rec)+".h5")
    test_on_data(corpus,maxlen,model)
    rec+=2