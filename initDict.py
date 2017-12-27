import csv

with open("/home/ubuntu/thesiswork/data/abs0.txt.mentions","r",newline='') as csvfile:
	reader = csv.reader(csvfile)
	for item in reader:
		print(item)