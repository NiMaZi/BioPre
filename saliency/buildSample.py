import sys
import csv
import pickle

volume=int(sys.argv[1])

for i in range(0,volume):
	with open("/home/ubuntu/thesiswork/data/abs"+str(i)+".txt.mentions","r",newline='',encoding='utf-8') as csvfile:
		reader=csv.reader(csvfile)