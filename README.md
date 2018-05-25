BioPre is a supervised model using neural network with bag-of-words embedding to predict the entity mention in body of scientific article given the correspondint metadata including abstract and author information.

You can use:

train.py

to train a model with abstract-body pairs (author information is optional);

type "train.py -h" to check the usage.

You can use:

predict.py

to predict entity mentions in body with the model trained using train.py;

type "predict.py" to check the usage.

All the articles should be annotated to entity lists in *.csv format, and all the vocabularies should be in *.json format.

Have problems? Look into the code by yourself!

More problems or want the training data/optimized models? Contact me througt zhengyl940425@gmail.com!