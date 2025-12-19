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
latest_posts:
  enabled: true
  scrollable: false # adds a vertical scroll bar if there are more than 3 new posts items
  limit: 3 # leave blank to include all the blog posts
---

<!-- Hero Section with Clean Design -->
<div class="hero-section">
  <div class="container-fluid px-4 py-3">
    <div class="row align-items-center">
      <div class="col-lg-9 col-md-8">
        <div class="hero-content">
          <p class="hero-description mb-0">
            The <strong>Spectrum Lab</strong> is a research group led by 
            <a href="https://ee.iisc.ac.in/chandra-sekhar-seelamantula/" class="text-decoration-none">Prof. Chandra Sekhar Seelamantula</a> 
            in the <a href="https://ee.iisc.ac.in/" class="text-decoration-none">Department of Electrical Engineering</a> 
            at the <a href="https://iisc.ac.in/" class="text-decoration-none">Indian Institute of Science</a>. 
            The lab focuses on problems in the intersection of computational imaging and machine learning.
          </p>
        </div>
      </div>
      <div class="col-lg-3 col-md-4 text-center">
        <div class="hero-logos">
          <div class="logo-item">
            <a href="https://iisc.ac.in" target="_blank" rel="noopener noreferrer" title="Indian Institute of Science">
              {% include figure.liquid 
                path='assets/img/logo/iisc/IISc_Seal_Master_logo_Black.png' 
                alt="Indian Institute of Science" 
                class="logo-img iisc-logo iisc-logo-light"
              %}
              {% include figure.liquid 
                path='assets/img/logo/iisc/IISc_Seal_Master_logo_White.png' 
                alt="Indian Institute of Science" 
                class="logo-img iisc-logo iisc-logo-dark"
              %}
            </a>
          </div>
          <div class="logo-item">
            <a href="https://ee.iisc.ac.in" target="_blank" rel="noopener noreferrer" title="Department of Electrical Engineering, IISc">
              {% include figure.liquid 
                path='assets/img/logo/iisc/ee_logo.png' 
                alt="Department of Electrical Engineering" 
                class="logo-img ee-logo"
              %}
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<div class="row mt-4">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid path='assets/img/album/random-collection/18.jpg' alt="Spectrum Lab members at ICASSP 2025 in Hyderabad, India" title="ICASSP 2025" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Spectrum Lab, past and present, at <a href="https://2025.ieeeicassp.org/">ICASSP 2025</a>, in Hyderabad, India.
</div>

<!-- Custom Lab Director Section with Side-by-Side Layout -->
<div class="lab-director-section">
  <h2 class="category">Lab Director</h2>
  {%- assign css_profile = site.people | where: "category", "Lab Director" | first -%}
  {%- if css_profile and css_profile.show -%}
    <div class="row align-items-center">
      <!-- Left column: Profile image and basic info -->
      <div class="col-md-4 text-center">
        <div class="profile-card">
          {%- if css_profile.img %}
            <a href="{{ css_profile.url | relative_url }}">
              {%- include figure.liquid
                path=css_profile.img
                alt="Prof. Chandra Sekhar Seelamantula, Lab Director"
                class="img-fluid rounded-circle z-depth-1 mb-3 profile-image"
              -%}
            </a>
          {%- endif %}
          <h2 class="card-title font-weight-bold mb-2">
            <a href="{{ css_profile.url | relative_url }}" class="text-decoration-none">
              {{ css_profile.firstname }} {{ css_profile.lastname }}
            </a>
          </h2>
          <p class="text-muted mb-3 text-center">{{ css_profile.description }}</p>
          
          <!-- Contact icons -->
          <div class="card-icons">
            {%- if css_profile.email -%}
              <a href="mailto:{{ css_profile.email | encode_email }}" title="e-mail">
                <i class="icon me-1 p-0 fas fa-envelope"></i>
              </a>
            {% endif %}
            {%- if css_profile.scholar_userid -%}
              <a href="https://scholar.google.com/citations?user={{ css_profile.scholar_userid }}" title="Google Scholar">
                <i class="icon me-1 p-0 ai ai-google-scholar"></i>
              </a>
            {% endif %}
          </div>
        </div>
      </div>
      
      <!-- Right column: Biography -->
      <div class="col-md-8">
        <div class="biography-content">
          <div class="biography-text">
            <p>
              Chandra Sekhar Seelamantula is a <strong>Professor</strong> in the Department of Electrical Engineering at the Indian Institute of Science (IISc), Bangalore. He received his Bachelor of Engineering degree with <em>Prof. K. K. Nair Gold Medal</em> from Osmania University in 1999 and Ph.D. from IISc in 2005.
            </p>
            <p>
              After completing postdoctoral research at EPFL, Switzerland (2006–2009), he joined IISc as faculty in 2009 and now leads the <strong>Spectrum Lab</strong>. His research interests include signal processing, machine learning, Generative AI, computational imaging, and AI for Healthcare.
            </p>
            <p>
              He has served in various editorial roles including Senior Area Editor for IEEE Signal Processing Letters and Associate Editor for IEEE Transactions on Image Processing. He is a recipient of multiple awards including the Grand Challenges Exploration Award from Gates Foundation and the Qualcomm Innovation Fellowship.
            </p>
            <p class="read-more-link">
              <a href="{{ css_profile.url | relative_url }}" class="btn btn-outline-primary btn-sm">
                Read Full Profile →
              </a>
            </p>
          </div>
        </div>
      </div>
    </div>
  {%- endif -%}
</div>
