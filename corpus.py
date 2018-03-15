import os
import boto3
import json
import jsonlines
import csv
import subprocess

homedir=os.environ['HOME']
s3 = boto3.resource("s3")
sourceBucket=s3.Bucket('papers.scitodate.com')
targetBucket=s3.Bucket('workspace.scitodate.com')

def get_annotation(_inpath):
    subprocess.call(['java','-jar',homedir+'/ner/NobleJar/NobleCoder-1.0.jar','-terminology','NCI_Thesaurus','-input',_inpath,'-output',homedir+'/thesiswork/disambiguation','-search','best-match','-selectBestCandidates'])
    f=open(homedir+'/thesiswork/disambiguation/RESULTS.tsv','r',encoding='utf-8')
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
    f=open(homedir+'/thesiswork/annotation.csv','w',encoding='utf-8')
    wr=csv.writer(f)
    for row in result_list:
        wr.writerow(row)
    f.close()
    _outpath=homedir+'/thesiswork/annotation.csv'
    return _outpath

def upload_to_S3(_inpath,_fname,_counter,_format):
    f=open(_inpath,"r",encoding='utf-8')
    data=f.read()
    f.close()
    targetBucket.put_object(Body=data,Key="yalun/annotated_papers_with_txt/"+_fname+str(_counter)+"."+_format)

counter=0
logf=open(homedir+"/results/logs/annotator_log.txt",'a')
for i,item in enumerate(sourceBucket.objects.all()):
    if i<71:
        continue
    logf.write("source file "+str(i)+"\n")
    sourceBucket.download_file(item.key,homedir+"/thesiswork/source/papers/"+item.key)
    with jsonlines.open(homedir+"/thesiswork/source/papers/"+item.key) as reader:
        for record in reader:
            txt_path=homedir+"/thesiswork/tempdoc.txt"

            output=record['abstract']
            if not output:
                continue
            f=open(txt_path,"w",encoding='utf-8')
            f.write(output)
            f.close()
            upload_to_S3(txt_path,"abs",counter,"txt")
            path=get_annotation(txt_path)
            upload_to_S3(path,"abs",counter,"csv")
            
            output=record['body']
            if not output:
                continue
            f=open(txt_path,"w",encoding='utf-8')
            f.write(output)
            f.close()
            upload_to_S3(txt_path,"body",counter,"txt")
            path=get_annotation(txt_path)
            upload_to_S3(path,"body",counter,"csv")
            
            output=record['title']
            f=open(txt_path,"w",encoding='utf-8')
            f.write(output)
            f.close()
            upload_to_S3(txt_path,"title",counter,"txt")
            path=get_annotation(txt_path)
            upload_to_S3(path,"title",counter,"csv")
            
            counter+=1
logf.close()