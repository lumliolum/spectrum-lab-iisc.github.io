---
layout: page
title: People
permalink: /people/
subtitle:
nav: true
nav_order: 8
dropdown: true
children:
  - title: PhD Students
    permalink: /people/phd-students/
  - title: M.Tech Students
    permalink: /people/mtech-students/
  - title: M.Tech Research Students
    permalink: /people/mtech-research/
  - title: divider
  - title: PhD Graduates
    permalink: /people/phd-graduates/
  - title: M.Tech Graduates
    permalink: /people/mtech-graduates/
  - title: M.Tech Research Graduates
    permalink: /people/mtech-research-graduates/
  - title: divider
  - title: Research Associates
    permalink: /people/research-associates/
  - title: Project Associates
    permalink: /people/project-associates/
  - title: Interns
    permalink: /people/interns/
  - title: divider
  - title: Post Doc
    permalink: /people/post-doc/
  - title: divider
  - title: Administrator
    permalink: /people/administrator/
display_categories: [PhD Students, M.Tech Students, M.Tech Research Students, PhD Graduates, M.Tech Graduates, M.Tech Research Graduates, Research Associates, Post Doc, Project Associates, Administrator]
horizontal: true
---

<!-- pages/people.md -->
<div class="people">
  <!-- Display categorized people except Alumni -->
  {%- for category in page.display_categories %}
      <!-- <h2 class="category">{{ category }}</h2> -->
      {%- assign categorized_people = site.people | where: "category", category -%}
      {%- if category contains "Graduates" or category contains "Post Doc" or category contains "Interns" or category contains "Research Associates" or category contains "Project Associates" -%}
        {%- assign sorted_people = categorized_people | sort: "year" | reverse -%}
      {%- else -%}
        {%- assign sorted_people = categorized_people | sort: "title" -%}
      {%- endif -%}
      <h2 style="text-align: right;">{{ category }}</h2>    <hr>
      <div class="grid">
        {%- for person in sorted_people -%}
          {%- if person.show -%}
            {% include people.liquid person=person %}
          {%- endif -%}
        {%- endfor %}
      </div>
  {%- endfor %}
</div>
