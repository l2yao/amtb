---
sidebar_position: {{ pos }}
---


# {{ name }}

| 课程 | 代码 |
|------|-----|
{% for course in courses %}| {{ course.name }} | {{ course.code }} |
{% endfor %}