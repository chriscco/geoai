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


def file_getter(path):
    # get files under a path with specified extension
    files = [glob(path + extension) for extension in ['*.txt', '*.pdf']]
    return files


def text_getter(file_path):
    files = file_getter(file_path)
    txt_files = files[0]
    pdf_files = files[1]
    texts = []
    for file in txt_files:
        texts.append(text_reader(file))
    for file in pdf_files:
        texts.append('\n'.join(pdf_reader(file)))
    return texts


def text_reader(filename):
    f = open(filename, 'r')
    content = f.read()
    f.close()
    return content


def pdf_reader(filename):
    reader = PyPDF2.PdfReader(filename)
    return [page.extract_text() for page in reader.pages]


if __name__ == '__main__':
    text_getter('documents/')

# CITE: https://products.documentprocessing.com/merger/python/pypdf/

