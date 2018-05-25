import json

def load_sups(path):
	f=open(path,'r',encoding='utf-8')
	content=json.load(f)
	f.close()
	return content