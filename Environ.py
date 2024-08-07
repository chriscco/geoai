from dotenv import load_dotenv
import os


class Environ:
    def __init__(self):
        load_dotenv()

    def get_api_key(self):
        return os.environ.get("NEW_API_KEY")

    def get_directory(self):
        return os.environ.get("DIRECTORY")

    def get_upload_directory(self):
        return os.environ.get("UPLOAD_DIRECTORY")

    def get_openai_url(self):
        return os.environ.get("OPENAI_URL")