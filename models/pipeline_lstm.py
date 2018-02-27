import json
import numpy as np
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Reshape
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

def get_emb(code):
    e_vec=list(e2v_model.wv[code])
    n_vec=n2v_model[str(c2id[prefix+code])]
    return e_vec+n_vec

