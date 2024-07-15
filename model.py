import os

from openai import OpenAI
import config as cf
from documents import abstract
import os

# CITE: https://cookbook.openai.com/examples/vector_databases/elasticsearch/elasticsearch-retrieval-augmented-generation
# CITE: https://github.com/openai/openai-python
# CITE: https://ledgerbox.io/blog/rag-techniques-function-calling

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))


def pdf_loader(filename):
    # to be implemented
    return 1


def create_es_with_mapping(es, index_name):
    mapping = {
        "mappings": {
            "properties": {
                "model": {"type": "keyword"},
                "year": {"type": "keyword"},
                "text": {"type": "text"},
            }
        }
    }
    es.indices.create(index=index_name, mappings=mapping)


def toolkit_download():
    cf.nltk.download('punkt')  # cutting words
    cf.nltk.download('stopwords')


# convert input string to stemmed, tokenized keywords
def to_keywords(input_string):
    output_string = ""
    toolkit_download()
    no_symbols_string = cf.re.sub(r'[^a-zA-Z0-9\s]', ' ', input_string)
    word_tokens = cf.word_tokenize(no_symbols_string)
    stopwords = set(cf.stopwords.words('english'))
    stemmer = cf.PorterStemmer()
    # if word is not stopword, add to the output
    for word in word_tokens:
        if not word.lower() in stopwords:
            output_string += stemmer.stem(word) + " "
    return output_string


# initialize elasticsearch, add index to the instance es
def init_index(es, paragraphs):
    index_name = "index_name_temp"
    if es.indices.exist(index=index_name):
        es.indices.delete(index=index_name)
    create_es_with_mapping(es, index_name)

    actions = [
        {
            "_index": index_name,
            "_source": {
                "keywords": to_keywords(paras),
                "text": paras
            }
        }
        for paras in paragraphs
    ]
    # add the index to the instance of es
    cf.helpers.bulk(es, actions)


def search(es, query):
    top_n = 3  # number of records returned
    index_name = "index_name_temp"
    result = es.search(index=index_name, query=query, size=top_n)
    return [hit["_source"]["text"] for hit in result["hits"]["hits"]]


def get_response(question1, question2):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"},
            {"role": "user", "content": "Answer the following questions: "}
        ],
        temperature=0.5,
        stream=False,
    )
    return response.choices[0].message["content"]


def main():
    # Temporary
    paragraphs = range(100)
    paragraphs[0] = abstract.abstract_entry

    question1 = "How many properties are exposed to wildfire?"
    question2 = "What are the outcomes of a fire model?"


