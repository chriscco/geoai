
def get_mapping():
    mapping = {
        "properties": {
            "title": {
                "type": "text",
                "analyzer": "custom_analyzer"
            },
            "content": {
                "type": "text",
                "analyzer": "custom_analyzer"
            },
            "formula": {
                "type": "keyword"
            }
        }
    }
    return mapping


def get_setting():
    setting = {
        "analysis": {
            "analyzer": {
                "custom_analyzer": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["lowercase", "stop"]
                }
            }
        }
    }
    return setting

