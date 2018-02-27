import sys
import csv
import json
import numpy as np
from gensim.models import word2vec
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.callbacks import EarlyStopping
from keras.layers import Activation
from keras.layers import Dropout

path="/home/ubuntu/results_new/models/MLP.h5"
model=load_model(path)

