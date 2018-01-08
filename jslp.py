import json
import jsonlines

count=0
keyterms_count=0
keywords_count=0
with jsonlines.open("/home/ubuntu/pubmed_2017-05.jsonl") as reader:
	for item in reader:
		f=open("/home/ubuntu/thesiswork/kdata/keywords"+str(count)+".txt","w",encoding='utf-8')
		g=open("/home/ubuntu/thesiswork/kdata/title"+str(count)+".txt","w",encoding='utf-8')
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
		if str(keywords)=="None":
			continue
			# keywords_count=keywords_count+1
			# print(keywords)
		print(str(keywords))
		print(title)
		f.write(str(keywords))
		f.close()
		g.write(title)
		g.close()
		# if count==177:
		# 	print(json.dumps(item,sort_keys=False,indent=2,separators=(',',':')))
		# 	# print(str(body))
		# 	break
		count=count+1
		if count>5:
			break
	print(count)
	# print(count,keywords_count,keyterms_count)
