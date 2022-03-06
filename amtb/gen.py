import json
from os import listdir, path, makedirs
from jinja2 import Template
from pathlib import Path
from slugify import slugify

# Generate urls based on course
def generate_props(course):
    menuid_parent = course['menuidparent']
    menuid = course['menuid']
    if course['himp4'] == 1:
        course['baseURL'] = 'https://tw4.amtb.de/redirect/media/himp4/{}/{}/{}-'.format(menuid_parent, menuid, menuid)
        course['ext'] = 'mp4'
    elif course['mp4'] == 1:
        course['baseURL'] = 'https://tw4.amtb.de/redirect/media/mp4/{}/{}/{}-'.format(menuid_parent, menuid, menuid)
        course['ext'] = 'mp4'
    elif course['mp3'] == 1:
        course['baseURL'] = 'https://tw4.amtb.de/redirect/media/mp3/{}/{}/{}-'.format(menuid_parent, menuid, menuid)
        course['ext'] = 'mp3'

# Read mdx template
with open('template.mdx', 'r') as template:
    markdown_template = Template(template.read())

# Read json template
with open('template.json', 'r') as template:
    json_template = Template(template.read())

# Generating _category_.json
with open('_category_.json', 'w') as category:
    json_file = json_template.render({'label': 'AMTB', 'pos': 1})
    category.write(json_file)

# Create output dir if not exist
if not path.exists('output'):
    makedirs('output')
# Read menu.json for all dirs
with open('menu.json', 'r', encoding='utf-8') as menu:
    menus = json.load(menu)
    for categories in menus['categories']:
        for category in categories['categories']:
            dir = category['AMTB_NAME']
            files = listdir(dir)
            for file in files:
                base = Path(file).stem
                output_dir = 'output/' + dir + '/' + base
                makedirs(output_dir, exist_ok=True)
                with open(dir+'/'+file, 'r', encoding='utf-8') as f:
                    json_f = json.load(f)
                    for course in json_f['sutables']['data']:
                        menuid = course['menuid']
                        generate_props(course)
                        md_file = markdown_template.render(course)
                        with open(output_dir +'/' + menuid +'.mdx', 'w', encoding='utf-8') as wf:
                            wf.write(md_file)
