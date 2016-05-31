import xml.etree.ElementTree as ET
from collections import namedtuple
from os import listdir
from VSM import VSM

NamedText = namedtuple("Text", 'text, name')


def get_xml_text(filename, tag="text", stdout=False):
    for event, elem in ET.iterparse(filename):
        if event == "end" and elem.tag == tag:
            if stdout:
                print elem.tag, " ===> ", elem.text
            ret_value = elem.text
            elem.clear()
            return ret_value


def get_texts(stdout=False):
    # For one folder list of texts.
    text_list = []
    articles_path = "EMM-IR-Collection/Documents/"

    for f in listdir(articles_path):
        full_filename = articles_path + str(f)
        text_list.append(NamedText(get_xml_text(full_filename, stdout=stdout), str(f)))

    query_path = "EMM-IR-Collection/Queries/"
    query_list = []
    for f in listdir(query_path):
        full_filename = query_path + str(f)
        with open(full_filename, 'r') as my_file:
            query_text = my_file.read()
        query_list.append(NamedText(query_text, str(f)))

    return text_list, query_list


def main():
    texts, queries = get_texts()
    vsm = VSM(texts)
    results = vsm.retrieveArticles(queries[0])

main()
