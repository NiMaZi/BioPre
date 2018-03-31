import os
import boto3
import json
import jsonlines
import csv
import subprocess

homedir=os.environ['HOME']
s3 = boto3.resource("s3")
sourceBucket=s3.Bucket('workspace.scitodate.com')
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
    targetBucket.put_object(Body=data,Key="yalun/annotated_papers_authors/"+_fname+str(_counter)+"."+_format)

logf=open(homedir+"/results/logs/annotator_log_authors.txt",'a')
for i in range (57380,200000):
    try:
        sourceBucket.download_file("yalun/annotated_papers_authors/abs"+str(i)+".txt",homedir+"/thesiswork/source/papers/tmp.txt")
        txt_path=homedir+"/thesiswork/source/papers/tmp.txt"
        path=get_annotation(txt_path)
        upload_to_S3(path,"abs",i,"csv")

        sourceBucket.download_file("yalun/annotated_papers_authors/body"+str(i)+".txt",homedir+"/thesiswork/source/papers/tmp.txt")
        txt_path=homedir+"/thesiswork/source/papers/tmp.txt"
        path=get_annotation(txt_path)
        upload_to_S3(path,"body",i,"csv")

        sourceBucket.download_file("yalun/annotated_papers_authors/title"+str(i)+".txt",homedir+"/thesiswork/source/papers/tmp.txt")
        txt_path=homedir+"/thesiswork/source/papers/tmp.txt"
        path=get_annotation(txt_path)
        upload_to_S3(path,"title",i,"csv")
        logf.write("source file "+str(i)+"\n")
    except:
        pass
logf.close()