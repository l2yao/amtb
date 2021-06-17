import json
from os import listdir, path, makedirs
from jinja2 import Template
from pathlib import Path
from slugify import slugify

# Generate urls based on course
def generate_urls(course):
    urls = []
    number = course['numbers']
    menuid_parent = course['menuidparent']
    menuid = course['menuid']
    for episode in range(1, number+1):
        episode = str(episode).zfill(4)
        if course['himp4'] == 1:
            urls.append('https://tw4.amtb.de/redirect/media/himp4/{}/{}/{}-{}.mp4'.format(menuid_parent, menuid, menuid, episode))
        elif course['mp4'] == 1:
            urls.append('https://tw4.amtb.de/redirect/media/mp4/{}/{}/{}-{}.mp4'.format(menuid_parent, menuid, menuid, episode))
        elif course['mp3'] == 1:
            urls.append('https://tw4.amtb.de/redirect/media/mp3/{}/{}/{}-{}.mp3'.format(menuid_parent, menuid, menuid, episode))
    return urls

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
with open('menu.json', 'r') as menu:
    menus = json.load(menu)
    for categories in menus['categories']:
        for category in categories['categories']:
            dir = category['AMTB_NAME']
            files = listdir(dir)
            for file in files:
                base = Path(file).stem
                output_dir = 'output/' + dir + '/' + base
                makedirs(output_dir, exist_ok=True)
                with open(dir+'/'+file, 'r') as f:
                    json_f = json.load(f)
                    for course in json_f['sutables']['data']:
                        menuid = course['menuid']
                        course['urls'] = generate_urls(course)
                        md_file = markdown_template.render(course)
                        with open(output_dir +'/' + menuid +'.mdx', 'w') as wf:
                            wf.write(md_file)
