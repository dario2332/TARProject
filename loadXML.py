import xml.etree.ElementTree as ET
import re
from os import listdir
from os.path import isfile
from collections import namedtuple
from VSM import VSM

Text = namedtuple('Text', 'name, text')

def get_xml_text(filename, tag="Text", stdout=False):
    for event, elem in ET.iterparse(filename):
        if event == "end" and elem.tag == tag:
            if stdout: print elem.tag, " ===> ", elem.text
            ret_value = elem.text
            elem.clear()
            return ret_value

def get_texts(stdout=False):
    # For one folder list of texts.
    text_list = []
    for num in range(1, 2):
        folder_name = "Query" + str(num)
        path = "emm-test-collection/" + folder_name

        query_name = "Empty"
        for f in listdir(path):
            if re.match("^realquery*", str(f)): query_name = str(f)
            if not re.match("^article-*", str(f)): continue
            full_filename = path + "/" + str(f)
            text_list.append(Text(str(f), get_xml_text(full_filename, stdout=stdout)))

        full_queryname = path + "/" + query_name
        query = (Text(query_name, get_xml_text(full_queryname, stdout=stdout)))

    return text_list, query


def main():
    vsm = VSM()
    texts, query = get_texts()
    vsm.createVocabulary(texts)
    print map(lambda key: (key[0].name, key[1]), vsm.retrieveArticles(query))
    # print texts[0].text
    # print len(texts)

main()