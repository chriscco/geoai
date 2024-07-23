import nltk
import re
import os
import json
import PyPDF2
from glob import glob
from dotenv import load_dotenv
from elasticsearch7 import Elasticsearch, helpers
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


def get_api_key():
    load_dotenv()
    return os.environ.get("OPENAI_API_KEY")


def setup_elasticsearch():
    return Elasticsearch("http://localhost:9200")


def print_json(response) :
    json_str = json.dumps(response, indent=2)
    print(json_str)


def file_retrieve(path):
    # get files under a path with specified extension
    files = [glob(path + extension) for extension in ['*.text', '*.txt', '*.pdf']]
    return files


def source_loader(file_path):
    files = file_retrieve(file_path)
    txt_files = []
    for i in range(2):
        if files[i]:  # check if empty
            txt_files.append(files[i])
    pdf_files = [files[2]]
    texts = []
    for file in txt_files:
        for filename in file:
            texts.append(text_reader(filename))
    for file in pdf_files[0]:
        texts.append(pdf_reader(file))
    print(texts)


def text_reader(filename):
    f = open(filename, 'r')
    content = f.read()
    f.close()
    return content


def pdf_reader(filename):
    reader = PyPDF2.PdfReader(filename)
    return [page.extract_text() for page in reader.pages]


if __name__ == '__main__':
    source_loader("documents/")


