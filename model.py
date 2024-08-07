import json
import sys

from openai import OpenAI
import config as cf

client = OpenAI(
    api_key=cf.enviro.get_api_key(),
    base_url=cf.enviro.get_openai_url(),
)


def paragraph_builder(text):
    paragraphs = []
    lines = text.split('\n')
    for line in lines:
        if line:
            paragraphs.append(line)
    return paragraphs


# convert input string to stemmed, tokenized keywords
def to_keywords(input_string):
    output_string = ""
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
    #  retrieve mapping and setting
    es.indices.create(index=index_name, mappings=cf.get_mapping(), settings=cf.get_setting())

    actions = [
        {
            "_index": index_name,
            "_source": {
                "content": paras
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
        "multi_match": {
            "query": query,
            "fields": ["title", "content"]
        }
    }
    es.indices.refresh(index=index_name)
    response = es.search(index=index_name, query=query_keywords, size=top_n)
    return [hit["_source"]['content'] for hit in response["hits"]["hits"]]


def get_response(es, query):
    new_line = '\n'
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"},
            {"role": "user", "content":
                f"Please answer the following question based on the text below: "
                f"\nQuestion: {query}\nText: \n{new_line.join(search(es, query))}"}
        ],
        max_tokens=500,
        stream=False,
    )
    return completion.choices[0].message.content


if __name__ == '__main__':
    query = sys.argv[1]  # user prompt
    ifUpload = sys.argv[2]  # if a file is uploaded
    directory = cf.enviro.get_directory()
    upload_directory = cf.enviro.get_upload_directory()

    paragraphs = []
    if ifUpload == "true":
        paragraphs = paragraph_builder('\n'.join(cf.text_getter(upload_directory)))
    else:
        paragraphs = paragraph_builder('\n'.join(cf.text_getter(directory)))  # read documents by line

    es = cf.setup_elasticsearch()
    init_index(es, paragraphs)

    print(get_response(es, query))

    if ifUpload == "true":  # remove pdf file uploaded
        cf.os.remove(upload_directory + "upload.pdf")


# CITE: https://cookbook.openai.com/examples/vector_databases/elasticsearch/elasticsearch-retrieval-augmented-generation
# CITE: https://github.com/openai/openai-python
# CITE: https://ledgerbox.io/blog/rag-techniques-function-calling

