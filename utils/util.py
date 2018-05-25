import json

def load_sups(path):
	f=open(path,'r')
	cc2vid=json.load(f)
	f.close()
	return cc2vid