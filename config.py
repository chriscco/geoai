from elasticsearch import Elasticsearch, helpers
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import re


def setup_elasticsearch():
    return Elasticsearch("http://localhost:9200")