
from openai import OpenAI
import config as cf
from documents import abstract

client = OpenAI(api_key=cf.api_key)


def pdf_loader(filename):
    # to be implemented
    return 1


def paragraph_builder(text):
    paragraphs = []
    lines = text.split('\n')
    for line in lines:
        if line:
            paragraphs.append(line)
    return paragraphs


def create_es_with_mapping(es, index_name):
    mapping = {
        "properties": {
            "model": {
                "type": "keyword"
            },
            "text": {
                "type": "text"
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
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
    create_es_with_mapping(es, index_name)

    actions = [
        {
            "_index": index_name,
            "_source": {
                # needs to be re-constructed
                "keyword": to_keywords(paras),
                "text": paras
            }
        }
        for paras in paragraphs
    ]
    # add the index to the instance of es
    cf.helpers.bulk(es, actions)


def search(es, query):
    top_n = 10  # number of records returned
    index_name = "index_name_temp"
    query_keywords = {
        "match": {
            "keyword": to_keywords(query),
        }
    }
    es.indices.refresh(index=index_name)
    response = es.search(index=index_name, query=query_keywords, size=top_n)
    cf.print_json(response)
    return [hit["_source"]["text"] for hit in response["hits"]["hits"]]


def get_response(es, question1):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"},
            {"role": "user", "content": "Answer the following question: "
             + question1
             + "by using the following text:"
             + '\n'.join(search(es, question1))},
        ],
        temperature=0.5,
        stream=False,
    )
    return response.choices[0].message["content"]


if __name__ == '__main__':
    paragraphs = paragraph_builder(abstract.abstract_entry)

    es = cf.setup_elasticsearch()
    init_index(es, paragraphs)

    question1 = "what models were used?"

    # get_response(es, question1)

    search(es, question1)


# CITE: https://cookbook.openai.com/examples/vector_databases/elasticsearch/elasticsearch-retrieval-augmented-generation
# CITE: https://github.com/openai/openai-python
# CITE: https://ledgerbox.io/blog/rag-techniques-function-calling

