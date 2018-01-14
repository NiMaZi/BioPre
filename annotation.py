from time import time
from ner.ner.annotator.annotator import Annotator

_annotator = Annotator("ner/NobleJar/NobleCoder-1.0.jar","ner/NobleJar/Annotator.java",searchMethod="best-match",terminology="GAMUTS")

start=time()
for i in range(0,12935):
	_filename = "thesiswork/kdata/abs"+str(i)+".txt"
	_annotator.process(_filename)
	_filename = "thesiswork/kdata/body"+str(i)+".txt"
	_annotator.process(_filename)
	_filename = "thesiswork/kdata/title"+str(i)+".txt"
	_annotator.process(_filename)
	_filename = "thesiswork/kdata/keywords"+str(i)+".txt"
	_annotator.process(_filename)
end=time()

with open("log.txt","w") as log:
	log.write("time used: "+str(end-start)+" seconds")