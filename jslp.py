import json
import jsonlines

count=0
keyterms_count=0
keywords_count=0
with jsonlines.open("/home/ubuntu/pubmed_2017-05.jsonl") as reader:
	for item in reader:
		# f=open("/home/ubuntu/thesiswork/data/body"+str(count)+".txt","w",encoding='utf-8')
		# g=open("/home/ubuntu/thesiswork/data/abs"+str(count)+".txt","w",encoding='utf-8')
		# keylist=item.keys()
		abstract=item["abstract"]
		authors=item["authors"]
		title=item["title"]
		# units=item["units"]
		# keyterms=item["keyterms"]
		# ids=item["ids"]
		body=item["body"]
		keywords=item["keywords"]
		# date=item["date"]
		# _id=item["_id"]
		# if str(keyterms)!="None":
		# 	keyterms_count=keyterms_count+1
		# 	# print(keyterms)
		# if str(keywords)!="None":
		# 	keywords_count=keywords_count+1
			# print(keywords)
		print("hey\n")
		print(keywords)
		print("hey\n")
		print(title)
		# f.write(str(body))
		# f.close()
		# g.write(abstract)
		# g.close()
		# if count==177:
		# 	print(json.dumps(item,sort_keys=False,indent=2,separators=(',',':')))
		# 	# print(str(body))
		# 	break
		count=count+1
		if count>5:
			break
	print(count)
	# print(count,keywords_count,keyterms_count)
