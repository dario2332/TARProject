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
    texts, query = get_texts()
    vsm = VSM(texts)
    results = vsm.retrieveArticles(query)
    for res in results:
      print res[0].name, res[1]
    # print texts[0].text
    # print len(texts)

main()
