import numpy as np
from keras.models import Sequential, load_model
from keras.layers import LSTM, Bidirectional, Masking

sample=1024
length=290
dim=256

model=Sequential()
model.add(Masking(mask_value=0.0,input_shape=(length,dim)))
model.add(Bidirectional(LSTM(dim,return_sequences=False,activation="relu"),merge_mode='ave'))
model.compile(optimizer='nadam',loss='binary_crossentropy')

X=np.random.rand(sample,length,dim)
y=np.random.rand(sample,dim)

model.fit(X,y,batch_size=256,epochs=10)