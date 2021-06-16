import json
from jinja2 import Template

# Read mdx template
with open('template.mdx', 'r') as template:
    markdown_template = Template(template.read())

# Read json template
with open('template.json', 'r') as template:
    json_template = Template(template.read())

# Generating _category_.json
with open('_category_.json', 'w') as category:
    json_file = json_template.render({'label': 'Youtube', 'pos': 1})
    category.write(json_file)

# Generating course mdx based on template.mdx and data.json
with open('data.json', 'r') as f:
    data = json.load(f)
    for course in data['courses']:
        mdx = markdown_template.render(course)
        with open(course['name'] +'.mdx', 'w') as mdf:
            mdf.write(mdx)
