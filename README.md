# GeoAI
Updated 08/06/2024

## Server Repository
https://github.com/chriscco/geo_ai_server

## Introduction
This project is RAG model based which aims to 
solve the issues of the current AI models are lack of the 
knowledge in specific fields of study. GeoAI serves as a role to 
provide a more reliable and flexible AI model in the field of geography 
and environmental science.

GeoAI uses the API service from OpenAI to generate the response, the default 
API is GPT-3.5-turbo. 

## Installation
1. Get a free API Key at OpenAI
2. Clone the model repository 

    ```git clone https://github.com/chriscco/geoai.git```
    
3. Clone the server repository

    ```git clone https://github.com/chriscco/geo_ai_server.git```

4. Install Python Packages

    ```pip install -r /path/to/requirements.txt```

5. Install Elasticsearch using Homebrew

   1. ```brew tap elastic/tap```
   
   2. ```brew install elastic/tap/elasticsearch-full```

6. Install Maven and load ```pom.xml``` in server repository

7. Run the server

## Usage
The usage is nearly the same as ChatGPT, while GeoAI would generate
responses based on its dataset.

Users can upload one PDF file as reference to help GeoAI to generate
more accurate responses.

![ScreenShot](https://github.com/chriscco/geoai/blob/main/resources%20/screenshot1.png?raw=true)

## Built with
- [OpenAI](https://openai.com/)
- [SpringBoot](https://spring.io/projects/spring-boot)
- [JQuery](https://jquery.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Elasticsearch](https://www.elastic.co/)