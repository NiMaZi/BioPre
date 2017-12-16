import urllib2
import json
import os
import codecs
import pickle
from pprint import pprint
from time import time

REST_URL = "http://data.bioontology.org"
API_KEY = "d2808432-a47b-4321-b8f5-5819f06ee02b"

sample_result=[]

def get_json(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('Authorization', 'apikey token=' + API_KEY)]
    return json.loads(opener.open(url).read())

def print_annotations(annotations, get_class=True):
    # annotation=(str_class id, str_class name, strlist_[synonyms list], str_ontology id, str_ontology name, str_ontology acronym, [annotaion list])
    # annotation list=(str_text, str_match type, int_from, int_to)
    # f=open("parse.txt","w")
    count=0
    for result in annotations:
        # print "\tprocessing anno "+str(count)
        count=count+1
        class_details = get_json(result["annotatedClass"]["links"]["self"]) if get_class else result["annotatedClass"]
        # print "Class details"
        # print "\tid: " + class_details["@id"]
        # print "\tprefLabel: " + class_details["prefLabel"]
        # print "\tsynonyms: "
        # for syn in class_details["synonym"]:
        #     print syn+" "
        ontology_details = get_json(class_details["links"]["ontology"])
        # print "\tontology: " + ontology_details["name"] + "(" + ontology_details["acronym"] + ")"

        # print "Annotation details"
        annotation_list=[]
        for annotation in result["annotations"]:
            # print "\ttext: " + annotation["text"]
            # print "\tfrom: " + str(annotation["from"])
            # print "\tto: " + str(annotation["to"])
            # print "\tmatch type: " + annotation["matchType"]
            annotation_list.append((annotation["text"],annotation["matchType"],annotation["from"],annotation["to"]))

        sample_result.append((class_details["@id"],class_details["prefLabel"],class_details["synonym"],ontology_details["@id"],ontology_details["name"],ontology_details["acronym"],annotation_list))
        # if result["hierarchy"]:
        #     print "\n\tHierarchy annotations"
        #     for annotation in result["hierarchy"]:
        #         class_details = get_json(annotation["annotatedClass"]["links"]["self"])
        #         pref_label = class_details["prefLabel"] or "no label"
        #         print "\t\tClass details"
        #         print "\t\t\tid: " + class_details["@id"]
        #         print "\t\t\tprefLabel: " + class_details["prefLabel"]
        #         print "\t\t\tontology: " + class_details["links"]["ontology"]
        #         print "\t\t\tdistance from originally annotated class: " + str(annotation["distance"])

    print "finished"
        # print "\n\n"

text_to_annotate = "Melanoma is a malignant tumor of melanocytes which are found predominantly in skin but also in the bowel and the eye."

for i in range(1,10):
    print "processing file "+str(i)
    start=time()
    reader=open("E:/thesiswork/abs"+str(i)+".txt","r")
    # reader=codecs.open("E:/thesiswork/abs"+str(i)+".txt","r",encoding='utf-8')
    text_to_annotate=reader.read()
    # print text_to_annotate.decode('utf-8')
    reader.close()
    annotations = get_json(REST_URL + "/annotator?text=" + urllib2.quote(text_to_annotate))
    sample_result=[]
    print_annotations(annotations)
    print "writing text results"
    ss=open("E:/thesiswork/tupled_annotations_"+str(i)+".txt","w")
    ss.write("total: "+str(len(sample_result))+"\n\n")
    for k in sample_result:
        ss.write(str(k)+"\n\n")
    ss.close()
    print "writing pickle files"
    tt=open("E:/thesiswork/tupled_annotations_"+str(i)+".pickle","w")
    pickle.dump(sample_result,tt)
    tt.close()
    end=time()
    print "finished in "+str(end-start)+" seconds"


# Annotate using the provided text
# annotations = get_json(REST_URL + "/annotator?text=" + urllib2.quote(text_to_annotate))

# Print out annotation details
# print_annotations(annotations)

# ss=open("tupled_annotations.txt","w")
# ss.write("total: "+str(len(sample_result))+"\n\n")
# for i in sample_result:
#     ss.write(str(i)+"\n\n")
# ss.close()

# # Annotate with hierarchy information
# annotations = get_json(REST_URL + "/annotator?max_level=3&text=" + urllib2.quote(text_to_annotate))
# print_annotations(annotations)

# # Annotate with prefLabel, synonym, definition returned
# annotations = get_json(REST_URL + "/annotator?include=prefLabel,synonym,definition&text=" + urllib2.quote(text_to_annotate))
# print_annotations(annotations, False)