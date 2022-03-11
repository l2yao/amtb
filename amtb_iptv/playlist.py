import json
from jinja2 import Template
from os import listdir, path, makedirs
from pathlib import Path

# https://de1.amtb.de/vod/_definst_/mp4/02/02-002/02-002-0001.mp4/playlist.m3u8
def generate_link(course, index):
    menuid = course['menuid']
    menuidparent = course['menuidparent']
    mediatype = 'mp4'
    if course['mp4'] == '0':
        mediatype = 'mp3' # fallback to mp3 if mp4 is not available
    return 'https://vod.amtb.de/vod/_definst_/'+mediatype+'/'+menuidparent+'/'+menuid+'/'+menuid +'-'+str(index).zfill(4)+'.'+mediatype+'/playlist.m3u8'

with open('./template.m3u', 'r') as template:
    playlist_template = Template(template.read())

# Create output dir if not exist
if not path.exists('output'):
    makedirs('output')
# Read menu.json for all dirs
with open('../amtb/menu.json', 'r', encoding='utf-8') as menu:
    menus = json.load(menu)
    for categories in menus['categories']:
        for category in categories['categories']:
            dir = '../amtb/'+category['AMTB_NAME']
            files = listdir(dir)
            for file in files:
                base = Path(file).stem
                output_dir = 'output/' + category['AMTB_NAME'] + '/' + base
                makedirs(output_dir, exist_ok=True)
                with open(dir+'/'+file, 'r', encoding='utf-8') as f:
                    json_f = json.load(f)
                    for course in json_f['sutables']['data']:
                        classes = []
                        for index in range(course['numbers']):
                            newclass = {}
                            newclass['title'] = course['title'] + str(index+1)
                            newclass['link'] = generate_link(course, index+1)
                            classes.append(newclass)
                        playlist_file = playlist_template.render(classes=classes)
                        with open(output_dir +'/'+course['menuid']+'.m3u', 'w', encoding='utf-8') as wf:
                            wf.write(playlist_file)
