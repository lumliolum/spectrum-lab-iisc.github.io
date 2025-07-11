---
layout: about
title: about
permalink: /
subtitle:
nav_order: 0

profile:
  align: left
  image: ucmllogo-text.svg
  name: Calgary ML Lab
  image_circular: false # crops the image to make it circular

selected_papers: true # includes a list of papers marked as "selected={true}"
social: true # includes social icons at the bottom of the page

announcements:
  enabled: true # includes a list of news items
  scrollable: false # adds a vertical scroll bar if there are more than 3 news items
  limit: 3 # leave blank to include all the news in the `_news` folder
display_categories: [Lab Director, PhD Students, MSc Students, Undergraduates]
latest_posts:
  enabled: true
  scrollable: false # adds a vertical scroll bar if there are more than 3 new posts items
  limit: 3 # leave blank to include all the blog posts
---

The **Spectrum Lab**
is a research group led by [Prof. Chandra Sekhar Seelamantula](https://ee.iisc.ac.in/chandra-sekhar-seelamantula/) in the [Department of Electrical Engineering](https://ee.iisc.ac.in/) at the [Indian Institute of Science](https://iisc.ac.in/). The lab focuses on problems in the intersection of computational imaging and machine learning.

<div class="row">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/labphotos/neurips2024.jpg" title="NeurIPS 2024" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Spectrum had <a href="{{ 'assets/img/labphotos/icassp2025.jpg' | relative_url }}">3 different works being presented by 3 students</a> at the premier signal processing conference, <a href="https://2025.ieeeicassp.org/">ICASSP</a>, across the workshops and main conference.
</div>

<div class="row align-items-center">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/labphotos/lab_schulich_april2024.jpg" title="Schulich School of Engineering, University of Calgary" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Schulich School of Engineering, University of Calgary (April 2024)
        </div>
    </div>
    <div class="col-sm">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/labphotos/neurips2024.jpg" title="NeurIPS 2024" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            NeurIPS 2024, Vancouver, BC, Canada (December 2024)
        </div>
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid path="assets/img/labphotos/peyto2023.jpg" title="Peyto Lake, Banff National Park" class="img-fluid rounded z-depth-1" %}
        <div class="caption">
            Peyto Lake, Banff National Park, AB, Canada (August 2023)
        </div>
    </div>
    </div>
</div>

# People
<hr style="border-top: 1px solid #bbb;">

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
