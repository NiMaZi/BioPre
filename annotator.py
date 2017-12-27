from ner.ner.annotator.annotator import Annotator

_annotator = Annotator("ner/NobleJar/NobleCoder-1.0.jar","ner/NobleJar/Annotator.java",searchMethod="best-match",terminology="HIVO004")

for i in range(0,5):
	_filename = "thesiswork/data/abs"+str(i)+".txt"
	_annotator.process(_filename)
	_filename = "thesiswork/data/body"+str(i)+".txt"
	_annotator.process(_filename)