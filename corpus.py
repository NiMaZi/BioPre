import os
import boto3
import json
import jsonlines
import csv
import subprocess

s3 = boto3.resource("s3")
sourceBucket=s3.Bucket('papers.scitodate.com')
targetBucket=s3.Bucket('workspace.scitodate.com')

def get_annotation(_inpath):
    subprocess.call(['java','-jar','/home/ubuntu/ner/NobleJar/NobleCoder-1.0.jar','-terminology','NCI_Thesaurus','-input',_inpath,'-output','/home/ubuntu/thesiswork/kdata/disambiguation','-search','best-match','-selectBestCandidates'])
    f=open('/home/ubuntu/thesiswork/kdata/disambiguation/RESULTS.tsv','r',encoding='utf-8')
    unamb=f.read()
    f.close()
    tmp_list=unamb.split('\n')
    unamb_list=[]
    for item in tmp_list:
        unamb_list.append(item.split('\t'))
    result_list=[]
    result_list.append(['Mention','ConceptCode','ConceptName','SemanticType','Start'])
    unamb_list=unamb_list[1:len(unamb_list)-1]
    for item in unamb_list:
        result_list.append([item[1],item[2],item[3],item[4],item[5].split(',')[0].split('/')[1]])
    f=open('/home/ubuntu/thesiswork/kdata/annotation.csv','w',encoding='utf-8')
    wr=csv.writer(f)
    for row in result_list:
        wr.writerow(row)
    f.close()
    _outpath='/home/ubuntu/thesiswork/kdata/annotation.csv'
    return _outpath

def upload_to_S3(_inpath,_fname,_counter):
    f=open(_inpath,"r",encoding='utf-8')
    data=f.read()
    f.close()
    targetBucket.put_object(Body=data,Key="yalun/annotated_papers/"+_fname+str(_counter)+".csv")

counter=0
for i,item in enumerate(sourceBucket.objects.all()):
    print("source file "+str(i))
    sourceBucket.download_file(item.key,"/home/ubuntu/thesiswork/source/papers/"+item.key)
    with jsonlines.open("/home/ubuntu/thesiswork/source/papers/"+item.key) as reader:
        for record in reader:
            print("article "+str(counter))
            output=record['abstract']
            f=open("/home/ubuntu/thesiswork/kdata/tempdoc.txt","w",encoding='utf-8')
            f.write(output)
            f.close()
            path=get_annotation("/home/ubuntu/thesiswork/kdata/tempdoc.txt")
            upload_to_S3(path,"abs",counter)
            
            output=record['body']
            f=open("/home/ubuntu/thesiswork/kdata/tempdoc.txt","w",encoding='utf-8')
            f.write(output)
            f.close()
            path=get_annotation("/home/ubuntu/thesiswork/kdata/tempdoc.txt")
            upload_to_S3(path,"body",counter)
            
            output=record['title']
            f=open("/home/ubuntu/thesiswork/kdata/tempdoc.txt","w",encoding='utf-8')
            f.write(output)
            f.close()
            path=get_annotation("/home/ubuntu/thesiswork/kdata/tempdoc.txt")
            upload_to_S3(path,"title",counter)
            
            counter+=1