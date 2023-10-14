import requests
import os
from bs4 import BeautifulSoup
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

doc_type = ['.doc', '.pdf', '.txt', '.zip', '.epub']
base_url = 'http://ftp.budaedu.org/publish/'
executor = ThreadPoolExecutor(max_workers=4)

def isFile(link):
    filename, file_extension = os.path.splitext(link)
    if file_extension.lower() in doc_type:
        return True
    return False

def isDir(link):
    if len(link) > 1 and link[-1] == '/':
        return True
    return False

def download(file_url):
    file_name = file_url.replace(base_url, '')
    path = 'budaedu/' + file_name
    if os.path.exists(path):
        print('skipping '+file_url)
        return
    dirname = os.path.dirname(path)
    Path(dirname).mkdir(parents=True, exist_ok=True)
    print('downloading '+file_url)
    r = requests.get(file_url, allow_redirects=True)
    with open(path, 'wb') as wf:
        wf.write(r.content)

def parseURL(url):
    files = []
    dirs = []
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    for link in soup.find_all('a'):
        link_href = link.get('href')
        if isFile(link_href):
            files.append(url+link_href)
        if isDir(link_href):
            dirs.append(url+link_href)
    return files, dirs

urls = [base_url]
while len(urls) > 0:
    url = urls.pop(0)
    files, dirs = parseURL(url)
    for file in files:
        executor.submit(download, file)
    urls.extend(dirs)
