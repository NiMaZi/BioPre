from ner.ner.annotator.annotator import Annotator

_annotator = Annotator("ner/NobleJar/NobleCoder-1.0.jar","ner/NobleJar/Annotator.java",searchMethod="best-match",terminology="HIVO004")

_filename = "thesiswork/data/abs0.txt"

_annotator.process(_filename)
