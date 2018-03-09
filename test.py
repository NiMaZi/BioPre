# import numpy as np
# from keras.models import Sequential, load_model
# from keras.layers import LSTM, Bidirectional, Masking

# sample=1024
# length=290
# dim=256

# model=Sequential()
# model.add(Masking(mask_value=0.0,input_shape=(length,dim)))
# model.add(Bidirectional(LSTM(dim,return_sequences=False,activation="relu"),merge_mode='ave'))
# model.compile(optimizer='nadam',loss='binary_crossentropy')

# X=np.random.rand(sample,length,dim)
# y=np.random.rand(sample,dim)

# model.fit(X,y,batch_size=256,epochs=10)


import numpy as np
from keras import optimizers
from keras.models import Sequential,load_model
from keras.layers import Dense,Dropout,BatchNormalization
from keras.callbacks import EarlyStopping

dim=16384
hrate=1.5
drate=0.5

myAct='relu'
model=Sequential()
model.add(Dense(int(dim*hrate),input_dim=dim,activation=myAct))
model.add(BatchNormalization())
model.add(Dropout(drate))
model.add(Dense(dim,activation=myAct))
model.compile(optimizer='Nadam',loss='binary_crossentropy')

sample=1024
X=np.random.rand(sample,dim)
y=np.random.rand(sample,dim)

early_stopping=EarlyStopping(monitor='loss',patience=10)
model.fit(X,y,batch_size=256,epochs=100,shuffle=True,callbacks=[early_stopping])