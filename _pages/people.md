---
layout: page
title: People
permalink: /people/
subtitle:
nav: true
nav_order: 8
dropdown: true
children:
  - title: All People
    permalink: /people/
  - title: divider
  - title: PhD Students
    permalink: /people/phd-students/
  - title: Project Associates
    permalink: /people/project-associates/
  - title: M.Tech Students
    permalink: /people/mtech-students/
  - title: M.Tech Research Students
    permalink: /people/mtech-research/
  - title: PhD Graduates
    permalink: /people/phd-graduates/
  - title: M.Tech Research Graduates
    permalink: /people/mtech-research-graduates/
  - title: Administrator
    permalink: /people/administrator/
display_categories: [Administrator, PhD Students, Project Associates, M.Tech Students, M.Tech Research Students, PhD Graduates, M.Tech Research Graduates]
horizontal: true
---

<!-- pages/people.md -->
<div class="people">
  <!-- Display categorized people except Alumni -->
  {%- for category in page.display_categories %}
      <!-- <h2 class="category">{{ category }}</h2> -->
      {%- assign categorized_people = site.people | where: "category", category -%}
      {%- assign sorted_people = categorized_people | sort: "year" | reverse %}
      <h2 style="text-align: right;">{{ category }}</h2>    <hr>
      <div class="grid">
        {%- for person in sorted_people -%}
          {%- if person.show -%}
            <!-- Custom alumni display with current_position -->
            <div class="grid-item">
              {%- if person.redirect -%}
                <a href="{{ person.redirect }}">
              {%- else -%}
                <a href="{{ person.url | relative_url }}">
              {%- endif %}
                <div class="card hoverable">
                  {%- if person.img %}
                    {%- include figure.liquid
                      path=person.img
                      alt="Portrait"
                      class="img-fluid rounded-circle z-depth-0"
                    -%}
                  {%- endif %}
                  <h2 class="card-title text-capitalize">
                    {{ person.firstname }} {{ person.lastname }}
                  </h2>
                  {%- if person.current_position -%}
                    <h3 class="card-text mt-1 mb-2" style="font-size: 0.9rem; color: #666;">
                      {{ person.current_position }}
                    </h3>
                  {%- endif -%}
                  {%- if person.pronouns -%}
                    <h3 class="card-title card-pronouns mb-2">
                      {{ person.pronouns }}
                    </h3>
                  {%- endif -%}
                  <div class="card-icons">
                    {%- if person.email -%}
                      <a href="mailto:{{ person.email | encode_email }}" title="e-mail">
                        <i class="icon me-1 p-0 fas fa-envelope"></i>
                      </a>
                    {% endif %}
                    {%- if person.orcid_id -%}
                      <a href="https://orcid.org/{{ person.orcid_id }}" title="ORCID">
                        <i class="icon me-1 p-0 ai ai-orcid"></i>
                      </a>
                    {% endif %}
                    {%- if person.scholar_userid -%}
                      <a href="https://scholar.google.com/citations?user={{ person.scholar_userid }}" title="Google Scholar">
                        <i class="icon me-1 p-0 ai ai-google-scholar"></i>
                      </a>
                    {% endif %}
                    {%- if person.github_username -%}
                      <a href="https://github.com/{{ person.github_username }}" title="GitHub">
                        <i class="icon me-1 p-0 fab fa-github"></i>
                      </a>
                    {% endif %}
                    {%- if person.linkedin_username -%}
                      <a href="https://www.linkedin.com/in/{{ person.linkedin_username }}" title="LinkedIn">
                        <i class="icon me-1 p-0 fab fa-linkedin"></i>
                      </a>
                    {% endif %}
                    {%- if person.twitter_username -%}
                      <a href="https://twitter.com/{{ person.twitter_username }}" title="Twitter">
                        <i class="icon me-1 p-0 fab fa-twitter"></i>
                      </a>
                    {% endif %}
                    {%- if person.website -%}
                      <a href="{{ person.website }}" title="Website">
                        <i class="icon me-1 p-0 fas fa-globe"></i>
                      </a>
                    {% endif %}
                  </div>
                  <div class="card-body">
                    <!-- <h3 class="card-text mt-1">{{ person.description }}</h3> -->
                  </div>
                </div>
              </a>
            </div>
          {%- endif -%}
        {%- endfor %}
      </div>
  {%- endfor %}
</div>
