import json
import jsonlines

f=open("E:/thesiswork/test.txt","w")



count=0
with jsonlines.open("E:/thesiswork/pubmed_2017-05.jsonl") as reader:
	for item in reader:
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
		print(abstract)
		f.write(abstract)
		# print(json.dumps(item,sort_keys=True,indent=2,separators=(',',':')))
		count=count+1
		if count>0:
			break

f.close()