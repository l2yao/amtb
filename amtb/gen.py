import json
from os import listdir, path, makedirs
from jinja2 import Template
from pathlib import Path
from slugify import slugify

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
                with open(dir+'/'+file, 'r') as f:
                    json_f = json.load(f)
                    for course in json_f['sutables']['data']:
                        md_file = markdown_template.render(course)
                        output_dir = 'output/' + dir + '/' + base
                        makedirs(output_dir, exist_ok=True)
                        with open(output_dir +'/' + slugify(course['title'])+'.mdx', 'w') as wf:
                            wf.write(md_file)
