---
layout: page
title: Chandra Sekhar Seelamantula
firstname: Chandra Sekhar
lastname: Seelamantula
description: Professor
img: assets/img/people/lab_director/Chandra.jpg
redirect:
orcid_id: 
linkedin_username: 
github: 
email: css@iisc.ac.in
scholar_userid: 1g1i1B4AAAAJ
twitter_username: 
category: Lab Director
show: true
---

<div class="container my-5">
  <div class="row">
    <!-- Left column: Image and Contact Info -->
    <div class="col-md-4 text-center">
      <img src="{{ page.img | relative_url }}" alt="{{ page.firstname }} {{ page.lastname }}" class="img-fluid rounded shadow mb-3" style="max-height: 300px;">
      <h3 class="mt-3">{{ page.firstname }} {{ page.lastname }}</h3>
      <p class="text-muted mb-2">{{ page.description }}</p>

      {% if page.email %}
      <p><i class="bi bi-envelope-fill me-2"></i><a href="mailto:{{ page.email }}">{{ page.email }}</a></p>
      {% endif %}

      <div class="d-flex flex-wrap justify-content-center gap-2 mt-3">
        {% if page.orcid_id %}
        <a href="https://orcid.org/{{ page.orcid_id }}" target="_blank" class="btn btn-sm btn-outline-dark">ORCID</a>
        {% endif %}
        {% if page.scholar_userid %}
        <a href="https://scholar.google.com/citations?user={{ page.scholar_userid }}" target="_blank" class="btn btn-sm btn-outline-primary">Google Scholar</a>
        {% endif %}
        {% if page.linkedin_username %}
        <a href="https://linkedin.com/in/{{ page.linkedin_username }}" target="_blank" class="btn btn-sm btn-outline-info">LinkedIn</a>
        {% endif %}
        {% if page.github %}
        <a href="https://github.com/{{ page.github }}" target="_blank" class="btn btn-sm btn-outline-dark">GitHub</a>
        {% endif %}
        {% if page.twitter_username %}
        <a href="https://twitter.com/{{ page.twitter_username }}" target="_blank" class="btn btn-sm btn-outline-primary">Twitter</a>
        {% endif %}
      </div>
    </div>

    <!-- Right column: Biography and Visiting Positions -->
    <div class="col-md-8">
      <div class="card shadow-sm border-0 mb-4">
        <div class="card-body">
          <h5 class="card-title">Biography</h5>
          <p class="card-text">
            Chandra Sekhar Seelamantula (Senior Member, IEEE) received the <strong>Bachelor of Engineering</strong> degree with <em>Prof. K. K. Nair Gold Medal</em> and <em>Best Thesis Award</em> from Osmania University in 1999 and the <strong>Ph.D.</strong> from IISc in 2005 with an IBM India Research Lab Fellowship.
          </p>
          <p>
            From 2005–2006, he was a consultant at ESQUBE Communication Solutions. From 2006–2009, he was a Postdoctoral Fellow at the Biomedical Imaging Group, EPFL, Switzerland, focusing on tomography, splines, and sparse signal processing.
          </p>
          <p>
            Since 2009, he has been a Professor in the Electrical Engineering Department, IISc, leading the <strong>Spectrum Lab</strong>. His research interests include speech/image processing, compressed sensing, inverse problems, and machine learning.
          </p>

          <h6 class="mt-4">Academic and Editorial Roles</h6>
          <ul>
            <li>Chair, IEEE Signal Processing Society Bangalore Chapter (2017–2021)</li>
            <li>Senior Area Editor, IEEE Signal Processing Letters (2017–2021)</li>
            <li>Associate Editor, IEEE Transactions on Image Processing (2018–2022)</li>
            <li>Area Chair, ICASSP 2020; TC Member, IEEE Computational Imaging (2020–2023)</li>
          </ul>

          <h6 class="mt-4">Awards</h6>
          <ul>
            <li>Prof. Priti Shankar Teaching Award, IISc</li>
            <li>Digital Health Prize, NBEC 2018</li>
            <li>Grand Challenges Exploration Award, Gates Foundation + BIRAC, 2020</li>
            <li>Qualcomm Innovation Fellowship (4x), 2019–2022</li>
            <li>Outstanding Editorial Board Member, IEEE Trans. on Image Processing, 2022</li>
          </ul>
        </div>
      </div>

      <!-- Visiting Positions -->
      <div class="card shadow-sm border-0">
        <div class="card-body">
          <h5 class="card-title">Visiting Positions</h5>
          <ul class="list-group list-group-flush">
            <li class="list-group-item">
              <strong>UNAM, Mexico</strong> – Dec 2017<br>
              Hosts: Prof. Chavez Garcia, Prof. Cardenas-Soto
            </li>
            <li class="list-group-item">
              <strong>JKU Linz, Austria</strong> – June–July 2016<br>
              Hosts: Dr. Bettina Heise, Prof. Kurt Hingerl
            </li>
            <li class="list-group-item">
              <strong>Chinese University of Hong Kong</strong> – Aug 2014<br>
              Host: Prof. Thierry Blu
            </li>
            <li class="list-group-item">
              <strong>University of Vienna, Austria</strong> – May 2014<br>
              Host: Prof. Torsten Moeller
            </li>
            <li class="list-group-item">
              <strong>EPFL (Biomedical Optics Lab)</strong> – June–July 2013<br>
              Host: Prof. Theo Lasser
            </li>
            <li class="list-group-item">
              <strong>CUHK, Hong Kong</strong> – May–June 2012<br>
              Host: Prof. Thierry Blu
            </li>
            <li class="list-group-item">
              <strong>EPFL (Biomedical Imaging Group)</strong> – May–July 2011<br>
              Host: Prof. Michael Unser
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</div>

<style>
    html[data-theme="dark"] {
  body {
    background-color: #121212;
    color: #e0e0e0;
  }

  .card {
    background-color: #1e1e1e;
    color: #e0e0e0;
  }

  .card-body {
    background-color: inherit;
  }

  .list-group-item {
    background-color: #1e1e1e;
    color: #e0e0e0;
    border-color: #333;
  }

  .text-muted {
    color: #aaaaaa !important;
  }

  a {
    color: #90caf9;
  }

  a:hover {
    color: #ffffff;
  }

  .btn-outline-primary {
    border-color: #90caf9;
    color: #90caf9;
  }

  .btn-outline-primary:hover {
    background-color: #90caf9;
    color: #000;
  }

  .btn-outline-info {
    border-color: #4dd0e1;
    color: #4dd0e1;
  }

  .btn-outline-info:hover {
    background-color: #4dd0e1;
    color: #000;
  }

  .btn-outline-dark {
    border-color: #ccc;
    color: #ccc;
  }

  .btn-outline-dark:hover {
    background-color: #ccc;
    color: #000;
  }

  .shadow,
  .shadow-sm {
    box-shadow: 0 0.2rem 0.6rem rgba(0, 0, 0, 0.5) !important;
  }
}
</style>