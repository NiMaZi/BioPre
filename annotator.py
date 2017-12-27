from ner.annotator.annotator import Annotator

_annotator = Annotator("NobleJar/NobleCoder-1.0.jar","NobleJar/Annotator.java",searchMethod="best-match",terminology="HIVO004")

_filename = "data/body0.txt"

output = _annotator.process(_filename)

print(output)