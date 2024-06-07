import urllib
import os
import os
from urllib.request import urlretrieve
from src.file_reader import get_title
from src.AI_methods import summarization
from src.AI_methods import generate_fuzzy_description
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