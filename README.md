BioPre is a supervised model using neural network with bag-of-words embedding to predict the entity mention in body of scientific article given the correspondint metadata including abstract and author information.

You can use:

train.py

to train a model with abstract-body pairs (author information is optional);

type "train.py -h" to check the usage.

You can use:

predict.py

to predict entity mentions in body with the model trained using train.py;

type "predict.py -h" to check the usage.

All the articles should be annotated to entity lists in *.csv format, and all the vocabularies should be in *.json format.

Failed attemps are under failed_attempts folder consisting of a binary classifier, a LSTM model and some data making-up scripts.

Have problems? Look into the code by yourself!

More problems or want the training data/optimized models? Contact me through zhengyl940425@gmail.com!