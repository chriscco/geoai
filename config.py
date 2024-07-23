from elasticsearch7 import Elasticsearch, helpers
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import re
import os
import json

from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")


def setup_elasticsearch():
    return Elasticsearch("http://localhost:9200")


def print_json(response) :
    json_str = json.dumps(response, indent=2)
    print(json_str)

