
import sys
import urllib.request
from bs4 import BeautifulSoup
def read_url(url):
    with urllib.request.urlopen(url) as response:
        return response.read().decode('utf-8')
    
def get_title(url):
    html = read_url(url)
    soup = BeautifulSoup(html, 'html.parser')
    title_element = soup.find('h1', class_='title mathjax')
    if title_element:
        return title_element.text.replace('Title:', '')
    else:
        return None

import urllib
import os
import os
from urllib.request import urlretrieve
def download_pdf(url, filename):
    response = urllib.request.urlopen(url)
    file = open(filename, 'wb')
    file.write(response.read())
    file.close()

def create_folder(folder_name):
    folder_path = os.path.join('./', folder_name)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def create_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)
def make_folder(url):
    # Get the title of the URL
    title = get_title(url)

    # Create a new folder with the title as the name
    folder_path = create_folder(title.replace(" ","_"))

    # Download the content of the URL into the newly created folder
    file_path = os.path.join(folder_path, 'content.pdf')
    urlretrieve(url.replace("/abs/","/pdf/"), file_path)

    # Create a summary of the downloaded content
    summary = summarization(folder_path, title)

    # Get fuzzy descriptors of the downloaded content
    fuzzy_descriptors = generate_fuzzy_description(folder_path, title)

    # Create individual files for the summary and fuzzy descriptors
    create_file(os.path.join(folder_path, 'summary.txt'), summary)
    create_file(os.path.join(folder_path, 'fuzzy_descriptors.txt'), fuzzy_descriptors)

from openai import OpenAI
import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

def generate_text(system_prompt, prompt):
    key = open("openaikey","r").read()
    os.environ["OPENAI_API_KEY"] = key
    messages = messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )
    return response.choices[0].message.content

def summarization(doc,name):
    key = open("openaikey","r").read()
    os.environ["OPENAI_API_KEY"] = key
    documents = SimpleDirectoryReader(doc).load_data()
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()
    return query_engine.query("Document name: "+name+" Create me a indepth summerization of the doucment in about 250 words.").response

def generate_fuzzy_description(doc,name):
    key = open("openaikey","r").read()
    os.environ["OPENAI_API_KEY"] = key
    documents = SimpleDirectoryReader(doc).load_data()
    index = VectorStoreIndex.from_documents(documents)
    query_engine = index.as_query_engine()
    return query_engine.query("Given the name and the context Make me a few search prompts that this document would be a good match for seperate your lines with only newlines name: "+name).response

command = sys.argv[1]
if command== "create":
    url = sys.argv[2]
    make_folder(url)
    print("Folder created successfully")
elif command == "search":
    print("Search functionality not implemented yet")
else:
    print("Invalid command")