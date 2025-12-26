---
layout: default
title: M.Tech Research Graduates
permalink: /people/mtech-research-graduates/
category: M.Tech Research Graduates
description: M.Tech (Research) graduates from the Spectrum Lab
nav: false
---

<div class="post">
  <header class="post-header">
    <h1 class="post-title">M.Tech Research Graduates</h1>
    <h2 class="post-description">M.Tech (Research) graduates from the Spectrum Lab</h2>
  </header>

  <article>
    <div class="people">
      {%- assign categorized_people = site.people | where: "category", "M.Tech Research Graduates" -%}
      {%- assign sorted_people = categorized_people | sort: "year" | reverse -%}
      
      <div class="grid">
        {%- for person in sorted_people -%}
          {%- if person.show -%}
              <div class="grid-item">
                {%- if person.redirect -%}
                  <a href="{{ person.redirect }}">
                {%- else -%}
                  <a href="{{ person.url | relative_url }}">
                {%- endif %}
                  <div class="card hoverable">
                    {%- if person.img %}
                      {%- include responsive-image.liquid
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
                    <div class="card-icons">
                      {%- if person.email -%}
                        <a href="mailto:{{ person.email | encode_email }}" title="e-mail">
                          <i class="icon me-1 p-0 fas fa-envelope"></i>
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
                      {%- if person.website -%}
                        <a href="{{ person.website }}" title="Website">
                          <i class="icon me-1 p-0 fas fa-globe"></i>
                        </a>
                      {% endif %}
                    </div>
                  <div class="card-body"></div>
                </div>
              </a>
            </div>
          {%- endif -%}
        {%- endfor %}
      </div>
    </div>
  </article>
</div>
