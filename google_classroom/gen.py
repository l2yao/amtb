import json
from jinja2 import Template

# Read md template
with open('template.md', 'r') as template:
    markdown_template = Template(template.read())

with open('data.json', 'r') as f:
    data = json.load(f)
    md = markdown_template.render(data)
    with open(data['name'] +'.md', 'w') as mdf:
        mdf.write(md)