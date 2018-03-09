import numpy as np
from keras.models import Sequential
from keras.layers import Dense

length=4096
dim=1024

model=Sequential()
model.add(Dense(int(2*dim),input_dim=dim,activation='relu'))
model.add(Dense(dim,activation='relu'))
model.compile(optimizer='nadam',loss='binary_crossentropy')

X=np.random.rand(length,dim)
y=np.random.rand(length,dim)

model.fit(X,y,batch_size=256,epochs=10)