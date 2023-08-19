from concurrent.futures import ThreadPoolExecutor
import json
import urllib.request
from pathlib import Path

doc_type = ['doc', 'pdf']
executor = ThreadPoolExecutor(max_workers=4)

def download(url, path, filename):
    Path(path).mkdir(parents=True, exist_ok=True)
    for ext in doc_type:
        url_with_suffix = url + f'&docstype={ext}'
        with urllib.request.urlopen(url_with_suffix) as f:
            doc = f.read()
            with open(f'{path}/{filename}.{ext}', 'wb') as wf:
                wf.write(doc)


def download_all(menu):
    with open(menu, 'r', encoding='utf-8') as menu:
        menus = json.load(menu)
        for categories in menus['categories']:
            for category in categories['categories']:
                dir = category['AMTB_NAME']
                for file in category['categories']:
                    file_name = file['AMTB_NAME']
                    file_path = f'../amtb/{dir}/{file_name}.json'
                    executor.submit(download_menu, dir, file_path, file_name)
                    #download_menu(dir, file_path, file_name)

def download_menu(dir, file_path, file_name):
    with open(file_path, 'r', encoding='utf-8') as menu_file:
        menu_file = json.load(menu_file)
        for doc in menu_file['sutables']['data']:
            if doc['txt'] == 1:
                menu_id = doc['menuid']
                numbers = doc['numbers']
                for index in range(numbers):
                    number = str(index+1).zfill(4)
                    url = f'https://ft.amtb.cn/ft.php?sn={menu_id}-{number}'
                    download(url, f'../doc/{dir}/{file_name}/{menu_id}', f'{number}')

download_all('../amtb/menu.json')