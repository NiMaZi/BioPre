import os
import sys
import csv
import subprocess

# Mention,ConceptCode,ConceptName,Synonyms,Start,End

# Document	Matched Term	Code	Concept Name	Semantic Type	Annotations	Certainty	ContextualAspect	ContextualModality	Degree	Experiencer	Permanence	Polarity	Temporality

for i in range(0,10):
	subprocess.call(['java','-jar','/home/ubuntu/ner/NobleJar/NobleCoder-1.0.jar','-terminology','NCI_Thesaurus','-input','/home/ubuntu/thesiswork/kdata/abs'+str(i)+'.txt','-output','/home/ubuntu/thesiswork/kdata/disambiguation','-search','best-match','-selectBestCandidates'])
	f=open('/home/ubuntu/thesiswork/kdata/disambiguation/RESULTS.tsv','r',encoding='utf-8')
	unamb=f.read()
	f.close()
	tmp_list=unamb.split('\n')
	unamb_list=[]
	for item in tmp_list:
		unamb_list.append(item.split('\t'))
	f=open('/home/ubuntu/thesiswork/kdata/abs'+str(i)+'.txt.mentions','r',encoding='utf-8')
	rd=csv.reader(f)
	j=0
	result_list=[]
	result_list.append(['Mention','ConceptCode','ConceptName','Synonyms','Semantic Type','Start','End'])
	for item in rd:
		if item[1]==unamb_list[j][2]:
			result_list.append([item[0],item[1],item[2],item[3],unamb_list[j][4],item[4],item[5]])
			j+=1
	f.close()
	f=open('/home/ubuntu/thesiswork/kdata/abs'+str(i)+'.csv','w',encoding='utf-8')
	wr=csv.writer(f)
	for row in result_list:
		wr.writerow(row)
	f.close()
