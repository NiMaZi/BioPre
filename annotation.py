from time import time
from ner.ner.annotator.annotator import Annotator

_annotator = Annotator("ner/NobleJar/NobleCoder-1.0.jar","ner/NobleJar/Annotator.java",searchMethod="best-match",terminology="HIVO004")

start=time()
for i in range(0,21772):
	_filename = "thesiswork/data2/abs"+str(i)+".txt"
	_annotator.process(_filename)
	_filename = "thesiswork/data2/body"+str(i)+".txt"
	_annotator.process(_filename)
	_filename = "thesiswork/data2/title"+str(i)+".txt"
	_annotator.process(_filename)
	_filename = "thesiswork/data2/keywords"+str(i)+".txt"
	_annotator.process(_filename)
end=time()

with open("log.txt","w") as log:
	log.write("time used: "+str(end-start)+" seconds")