from elasticsearch7 import Elasticsearch, helpers
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import re
import os

from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")


def setup_elasticsearch():
    return Elasticsearch("http://localhost:9200")