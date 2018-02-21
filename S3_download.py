import boto3

s3 = boto3.resource("s3")
myBucket=s3.Bucket('workspace.scitodate.com')
volume=12935

for i in range(0,volume):
	myBucket.download_file("yalun/kdata/abs"+str(i)+".csv","/home/ubuntu/thesiswork/kdata/abs"+str(i)+".csv")
	myBucket.download_file("yalun/kdata/body"+str(i)+".csv","/home/ubuntu/thesiswork/kdata/body"+str(i)+".csv")
	myBucket.download_file("yalun/kdata/title"+str(i)+".csv","/home/ubuntu/thesiswork/kdata/title"+str(i)+".csv")
	myBucket.download_file("yalun/kdata/keywords"+str(i)+".csv","/home/ubuntu/thesiswork/kdata/keywords"+str(i)+".csv")