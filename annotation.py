import os
from ner.ner.annotator.annotator import Annotator

term_dir="/home/ubuntu/.noble/terminologies/"

term_list=[]
for file in os.listdir(term_dir):
	if file.split(".")[0]:
		term_list.append(file.split(".")[0])

# _annotator = Annotator("ner/NobleJar/NobleCoder-1.0.jar","ner/NobleJar/Annotator.java",searchMethod="best-match",terminology="GAMUTS")

annotator_list=[]
for term in term_list:
	print("buidling annotator with term "+term+".\n")
	_annotator = Annotator("ner/NobleJar/NobleCoder-1.0.jar","ner/NobleJar/Annotator.java",searchMethod="best-match",terminology=term)
	annotator_list.append(_annotator)


for i in range(0,2000): # max 12935
	cf_abs=open("/home/ubuntu/thesiswork/kdata/abs"+str(i)+".csv","a")
	cf_body=open("/home/ubuntu/thesiswork/kdata/body"+str(i)+".csv","a")
	cf_title=open("/home/ubuntu/thesiswork/kdata/title"+str(i)+".csv","a")
	cf_keywords=open("/home/ubuntu/thesiswork/kdata/keywords"+str(i)+".csv","a")
	for j in range(0,len(term_list)):
		# _annotator = Annotator("ner/NobleJar/NobleCoder-1.0.jar","ner/NobleJar/Annotator.java",searchMethod="best-match",terminology=term)
		
		_filename = "thesiswork/kdata/abs"+str(i)+".txt"
		annotator_list[j].process(_filename)

		f=open("/home/ubuntu/thesiswork/kdata/abs"+str(i)+".txt.mentions")
		_str=f.read()
		cf_abs.write(_str)
		f.close()

		_filename = "thesiswork/kdata/body"+str(i)+".txt"
		annotator_list[j].process(_filename)

		f=open("/home/ubuntu/thesiswork/kdata/body"+str(i)+".txt.mentions")
		_str=f.read()
		cf_body.write(_str)
		f.close()

		_filename = "thesiswork/kdata/title"+str(i)+".txt"
		annotator_list[j].process(_filename)

		f=open("/home/ubuntu/thesiswork/kdata/title"+str(i)+".txt.mentions")
		_str=f.read()
		cf_title.write(_str)
		f.close()

		_filename = "thesiswork/kdata/keywords"+str(i)+".txt"
		annotator_list[j].process(_filename)

		f=open("/home/ubuntu/thesiswork/kdata/keywords"+str(i)+".txt.mentions")
		_str=f.read()
		cf_keywords.write(_str)
		f.close()

	cf_abs.close()
	cf_body.close()
	cf_title.close()
	cf_keywords.close()


