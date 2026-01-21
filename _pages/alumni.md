---
layout: page
title: alumni
permalink: /alumni/
subtitle:
nav: true
nav_order: 6

display_categories: [Alumni]
horizontal: true
---

<style>
.people .grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
  align-items: flex-start;
  gap: 1rem;
}

.people .grid-item {
  display: flex;
  flex-direction: column;
  align-items: stretch;
}

.people .card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.people .card-body {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}
</style>

<!-- <hr style="border-top: 1px solid #bbb;"> -->

<!-- pages/people.md -->
<div class="people">
  <!-- Display categorized people except Alumni -->
  {%- for category in page.display_categories %}
      <!-- <h2 class="category">{{ category }}</h2> -->
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
  {%- endfor %}
</div>
