import json
import jsonlines

count=0
with jsonlines.open("E:/thesiswork/pubmed_2017-05.jsonl") as reader:
	for item in reader:
		# f=open("E:/thesiswork/abs"+str(count)+".txt","w",encoding='utf-8')
		# keylist=item.keys()
		abstract=item["abstract"]
		authors=item["authors"]
		title=item["title"]
		units=item["units"]
		keyterms=item["keyterms"]
		ids=item["ids"]
		body=item["body"]
		keywords=item["keywords"]
		date=item["date"]
		_id=item["_id"]
		if str(keyterms)!="None":
			print(keyterms)
		if str(keywords)!="None":
			print(keywords)
		# f.write(abstract)
		# f.close()
		# print(json.dumps(units,sort_keys=False,indent=2,separators=(',',':')))
		count=count+1
		if count>30000:
			break

