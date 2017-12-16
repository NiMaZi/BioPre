import urllib2
import json
import os
import codecs
from pprint import pprint

REST_URL = "http://data.bioontology.org"
API_KEY = "d2808432-a47b-4321-b8f5-5819f06ee02b"

sample_result=[]

def get_json(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('Authorization', 'apikey token=' + API_KEY)]
    return json.loads(opener.open(url).read())

def print_annotations(annotations, get_class=True):
    # annotation=(str_class id, str_class name, strlist_[synonyms list], str_ontology name, str_ontology acronym, [annotaion list])
    # annotation list=(str_text, str_match type, int_from, int_to)
    # f=open("parse.txt","w")
    count=0
    for result in annotations:
        print "processing anno "+str(count)
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

        sample_result.append((class_details["@id"],class_details["prefLabel"],class_details["synonym"],ontology_details["name"],ontology_details["acronym"],annotation_list))
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

# text_to_annotate = "The organ covering the body that consists of the dermis and epidermis."

text_to_annotate = "Melanoma is a malignant tumor of melanocytes which are found predominantly in skin but also in the bowel and the eye."

# text_to_annotate = "A term for diseases in which abnormal cells divide without control and can invade nearby tissues. Malignant cells can also spread to other parts of the body through the blood and lymph systems. There are several main types of malignancy. Carcinoma is a malignancy that begins in the skin or in tissues that line or cover internal organs. Sarcoma is a malignancy that begins in bone, cartilage, fat, muscle, blood vessels, or other connective or supportive tissue. Leukemia is a malignancy that starts in blood-forming tissue, such as the bone marrow, and causes large numbers of abnormal blood cells to be produced and enter the blood. Lymphoma and multiple myeloma are malignancies that begin in the cells of the immune system. Central nervous system cancers are malignancies that begin in the tissues of the brain and spinal cord. Also called cancer."

# text_to_annotate = "American Airlines is a founding member of Oneworld alliance, the third largest airline alliance in the world and coordinates fares, services, and scheduling with alliance partners British Airways, Iberia, and Finnair in the transatlantic market and with Cathay Pacific and Japan Airlines in the transpacific market. Regional service is operated by independent and subsidiary carriers under the brand name of American Eagle.[9]"

for i in range(0,20):
    reader=open("E:/thesiswork/abs"+str(i)+".txt","r")
    # reader=codecs.open("E:/thesiswork/abs"+str(i)+".txt","r",encoding='utf-8')
    # text_to_annotate=reader.read()
    # print text_to_annotate.decode('utf-8')
    reader.close()

# Annotate using the provided text
annotations = get_json(REST_URL + "/annotator?text=" + urllib2.quote(text_to_annotate))
# sample_result=get_json(REST_URL + "/annotator?text=" + urllib2.quote(text_to_annotate));
# for i in sample_result:
# 	print str(i)
# print str(len(sample_result))+"\n"


# g=open("annotation.txt","w")

# annotation_tuple=[]

# count=1
# for item in sample_result:
#     # print "result no. "+str(count)
#     # g.write("result no. "+str(count)+"\n")
#     for annotation in item["annotations"]:
#         # print "\ttext: " + str(annotation["text"])
#         # print "\tfrom: " + str(annotation["from"])
#         # print "\tto: " + str(annotation["to"])
#         # print "\tmatch type: " + annotation["matchType"]
#         # print "\n"
#         # g.write("text: " + annotation["text"]+", ")
#         # g.write("from: " + str(annotation["from"])+", ")
#         # g.write("to: " + str(annotation["to"])+", ")
#         # g.write("match type: " + annotation["matchType"]+"\n")
#         annotation_tuple.append((annotation["text"],annotation["matchType"]))
#     count=count+1
#     # print "\n"
# # g.close()
    
# annotation_tuple=list(set(annotation_tuple))

# print str(len(annotation_tuple))+"\n"
# for a in annotation_tuple:
#     print str(a)+"\n"

# print json.dumps(sample_result[0],sort_keys=True,indent=2,separators=(',',':'))

# print json.dumps(sample_result[0]["annotatedClass"],sort_keys=True,indent=2,separators=(',',':'))


# f=open("sample.txt","w")
# f.write(str(sample_result))
# f.close

# Print out annotation details
print_annotations(annotations)

print str(len(sample_result))
print str(sample_result)

# # Annotate with hierarchy information
# annotations = get_json(REST_URL + "/annotator?max_level=3&text=" + urllib2.quote(text_to_annotate))
# print_annotations(annotations)

# # Annotate with prefLabel, synonym, definition returned
# annotations = get_json(REST_URL + "/annotator?include=prefLabel,synonym,definition&text=" + urllib2.quote(text_to_annotate))
# print_annotations(annotations, False)