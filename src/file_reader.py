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

