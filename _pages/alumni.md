---
layout: page
title: Alumni
permalink: /alumni/
subtitle:
nav: true
nav_order: 6

display_categories: [PhD, MTech (Res.)]
horizontal: true
---

<style>
.people .grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
  align-items: stretch;
  gap: 1rem;
}

.people .grid-item {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  flex: 1 1 300px; /* Allow items to grow/shrink with minimum width */
  max-width: 350px; /* Prevent items from becoming too wide */
  height: 450px;
}

.people .card {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.people .card-body {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 1rem;
}

.people .card-title {
  margin-bottom: 0.5rem;
}

.people .card-icons {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  margin: 0.5rem 0;
}

.people .card-text {
  margin-top: 0.5rem;
  margin-bottom: 0;
}
</style>

<!-- <hr style="border-top: 1px solid #bbb;"> -->

<!-- pages/people.md -->
<div class="people">
  <!-- Display categorized people except Alumni -->
  {%- for category in page.display_categories %}
      <!-- <h2 class="category">{{ category }}</h2> -->
      {%- assign categorized_people = site.people | where: "description", category -%}
      {%- assign sorted_people = categorized_people | sort: "year" | reverse %}
      <h2 style="text-align: right;">{{ category }}</h2>    <hr>
      <div class="grid">
        {%- for person in sorted_people -%}
          {%- if person.show -%}
            {% include people.liquid %}
          {%- endif -%}
        {%- endfor %}
      </div>
  {%- endfor %}
</div>
