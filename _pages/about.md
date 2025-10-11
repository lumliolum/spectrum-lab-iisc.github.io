---
layout: about
title: Home
permalink: /
subtitle:
nav_order: 0

profile:
  align:
  image:
  name:
  image_circular: false # crops the image to make it circular

selected_papers: true # includes a list of papers marked as "selected={true}"
social: true # includes social icons at the bottom of the page

announcements:
  enabled: true # includes a list of news items
  scrollable: false # adds a vertical scroll bar if there are more than 3 news items
  limit: 3 # leave blank to include all the news in the `_news` folder
display_categories: [Lab Director]
latest_posts:
  enabled: true
  scrollable: false # adds a vertical scroll bar if there are more than 3 new posts items
  limit: 3 # leave blank to include all the blog posts
---

The **Spectrum Lab**
is a research group led by [Prof. Chandra Sekhar Seelamantula](https://ee.iisc.ac.in/chandra-sekhar-seelamantula/) in the [Department of Electrical Engineering](https://ee.iisc.ac.in/) at the [Indian Institute of Science](https://iisc.ac.in/). The lab focuses on problems in the intersection of computational imaging and machine learning.


<!-- pages/people.md -->
<div class="people">
  <!-- Display categorized people except Alumni -->
  {%- for category in page.display_categories %}
      <h2 class="category">{{ category }}</h2>
      {%- assign categorized_people = site.people | where: "category", category -%}
      {%- assign sorted_people = categorized_people | sort: "lastname" %}
      <!-- Generate cards for each person -->
      <div class="grid">
        {%- for person in sorted_people -%}
          {%- if person.show -%}
            {% include people.liquid %}
          {%- endif -%}
        {%- endfor %}
      </div>
  {% endfor %}
</div>
