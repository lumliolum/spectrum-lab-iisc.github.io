---
layout: page
title: Funding
permalink: /funding/
description:
nav: true
nav_order: 6
horizontal: false
---

{% include funding.liquid %}

<div class="projects">
  <div class="container">
    <div class="funding-grid">
      {% for project in site.data.funding.projects %}
      <div class="funding-card mb-4 p-3 hoverable">
        <div class="col-md-12">
          <h5 class="card-title mb-1" style="color: var(--global-theme-color) !important;">{{ project.title }}</h5>
          <h6 class="card-subtitle mb-3 text-muted">
            <i class="fa-solid fa-building-columns iconinstitution"></i> {{ project.agency }}
          </h6>
          <div class="card-text">
            <div class="row">
              <div class="col-md-6">
                <p class="mb-1"><i class="fa-solid fa-user-tie icondepartment"></i> <strong>Role:</strong> {{ project.role }}</p>
              </div>
              <div class="col-md-6">
                <p class="mb-1"><i class="fa-solid fa-calendar-days icondepartment"></i> <strong>Duration:</strong> {{ project.duration }}</p>
              </div>
            </div>
            {% if project.investigators %}
            <div class="row mt-2">
              <div class="col-md-12">
                <p class="mb-0"><i class="fa-solid fa-users icondepartment"></i> <strong>Co-Investigators:</strong> {{ project.investigators }}</p>
              </div>
            </div>
            {% endif %}
          </div>
        </div>
      </div>
      {% endfor %}
    </div>
  </div>
</div>

<style>
.funding-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}

@media (min-width: 768px) {
  .funding-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

.funding-card {
  border: 1px solid var(--global-divider-color);
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  background-color: var(--global-card-bg-color);
  border-radius: 8px;
  height: 100%;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.funding-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
</style>
