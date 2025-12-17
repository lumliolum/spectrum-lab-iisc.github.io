# 🌊 Spectrum Lab Website

Official website for **Spectrum Lab** at the Department of Electrical Engineering, Indian Institute of Science (IISc), Bengaluru.

🌐 **Live Site:** [spectrum-lab-iisc.github.io](https://spectrum-lab-iisc.github.io)

---

## 📖 Table of Contents

- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [How to Update Each Component](#-how-to-update-each-component)
  - [People / Team Members](#1-people--team-members)
  - [Publications](#2-publications)
  - [News & Announcements](#3-news--announcements)
  - [Teaching / Courses](#4-teaching--courses)
  - [Recognition & Awards](#5-recognition--awards)
  - [Funding / Sponsors](#6-funding--sponsors)
  - [Professional Activities](#7-professional-activities-lab-director)
  - [Projects](#8-projects)
  - [Photo Album](#9-photo-album)
- [Adding Images](#-adding-images)
- [Dark Mode Support](#-dark-mode-support)
- [Development](#-development)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)

---

## 🚀 Quick Start

### Prerequisites
- Ruby 3.x
- Bundler (`gem install bundler`)
- ImageMagick (for image processing)

### Local Development

```bash
# Clone the repository
git clone https://github.com/spectrum-lab-iisc/spectrum-lab-iisc.github.io.git
cd spectrum-lab-iisc.github.io

# Install dependencies
bundle install

# Start local server with live reload
JEKYLL_ENV=development bundle exec jekyll serve --livereload --port 8080

# Access at: http://localhost:8080
```

### Using Docker (Alternative)

```bash
docker-compose up --build
# Access at: http://localhost:8080
```

---

## 📁 Project Structure

```
spectrum-lab-iisc.github.io/
├── _bibliography/          # BibTeX publications
│   └── papers.bib          # All publications go here
├── _data/                  # YAML data files
│   ├── activities.yml      # Lab Director's professional activities
│   ├── funding.yml         # Funding sources/sponsors
│   ├── recognition.yml     # Awards and recognition
│   ├── teaching.yml        # Course listings
│   └── album.yaml          # Photo album categories
├── _includes/              # Reusable HTML/Liquid components
├── _layouts/               # Page templates
├── _news/                  # News announcements (markdown files)
├── _pages/                 # Static pages
├── _people/                # Team member profiles
│   ├── lab-director/       # Lab director profile
│   ├── phd-students/       # Current PhD students
│   ├── phd-graduates/      # PhD alumni
│   ├── mtech-students/     # Current MTech students
│   ├── mtech-research/     # MTech Research students
│   ├── project-associates/ # Project staff
│   └── person_template.md  # Template for new profiles
├── _projects/              # Research project pages
├── _sass/                  # SCSS stylesheets
├── assets/
│   └── img/                # All images
│       ├── people/         # Profile photos (organized by category)
│       ├── funders/        # Sponsor/funder logos
│       ├── recognition/    # Award photos
│       ├── album/          # Photo gallery images
│       └── logo/           # Lab logos
└── _config.yml             # Site configuration
```

---

## 📝 How to Update Each Component

### 1. People / Team Members

**Location:** `_people/[category]/`

**Categories (folders):**
- `lab-director/` - Lab director profile
- `phd-students/` - Current PhD students
- `phd-graduates/` - PhD alumni
- `mtech-students/` - Current MTech students
- `mtech-research/` - MTech Research students
- `mtech-research-graduates/` - MTech Research alumni
- `project-associates/` - Project staff
- `administrator/` - Administrative staff

#### Adding a New Person

1. **Copy the template:**
   ```bash
   cp _people/person_template.md _people/phd-students/firstname-lastname.md
   ```

2. **Add their photo:**
   - Save photo to `assets/img/people/[category]/filename.jpg`
   - Recommended: Square aspect ratio, at least 400x400px

3. **Edit the markdown file:**

```yaml
---
layout: person
title: John Doe
firstname: John
lastname: Doe
description: PhD Student
img: assets/img/people/phd-students/john-doe.jpg
email: johndoe@iisc.ac.in
scholar_userid: XXXXXXXX        # Google Scholar ID (optional)
linkedin_username: johndoe      # LinkedIn username (optional)
github: johndoe                 # GitHub username (optional)
orcid_id: 0000-0000-0000-0000   # ORCID ID (optional)
category: PhD Student
show: true                      # Set to false to hide

biography_paragraphs:
  - "First paragraph of biography..."
  - "Second paragraph..."

# Optional sections
show_awards: true
awards:
  - "Award 1, Year"
  - "Award 2, Year"
---
```

#### Removing or Hiding a Person

- **To hide temporarily:** Set `show: false` in the front matter
- **To remove:** Delete the markdown file (and optionally the photo)

#### Moving to Alumni

Move the file from `phd-students/` to `phd-graduates/` folder.

---

### 2. Publications

**Location:** `_bibliography/papers.bib`

#### Adding a New Publication

Add a BibTeX entry to `papers.bib`:

```bibtex
@article{author2025title,
  author      = {Author, A. and Author, B. and Seelamantula, C. S.},
  title       = {Paper Title Here},
  journal     = {IEEE Transactions on Signal Processing},
  year        = {2025},
  abbr        = {IEEE TSP 25},              # Short abbreviation shown on site
  url         = {https://link-to-paper},
  doi         = {10.1109/TSP.2025.XXXXX},
  bibtex_show = {true},                     # Show BibTeX button
  selected    = {true},                     # Feature on homepage
  code        = {https://github.com/...},   # Code repository (optional)
  pdf         = {paper.pdf},                # PDF in assets/pdf/ (optional)
  emails      = {author@iisc.ac.in}         # Links to author's page
}
```

**Key fields:**
| Field | Purpose |
|-------|---------|
| `abbr` | Short label (e.g., "ICASSP 25") |
| `selected` | `true` to show on homepage |
| `bibtex_show` | `true` to show copy BibTeX button |
| `emails` | Comma-separated emails to link authors |
| `code` | GitHub/code repository URL |
| `pdf` | PDF filename in `assets/pdf/` |

---

### 3. News & Announcements

**Location:** `_news/`

#### Adding News

Create a new markdown file with date prefix:

```bash
# Filename format: YYYY-MM-DD-short-title.md
touch _news/2025-01-15-new-paper.md
```

**Content:**

```yaml
---
layout: post
title: Paper Accepted at ICASSP 2025
date: 2025-01-15
inline: true                    # true = one-line, false = full post
related_posts: false
---

Our paper on [topic] was accepted at ICASSP 2025! 🎉
```

**Inline vs Full Post:**
- `inline: true` - Shows as a single line on the news page
- `inline: false` - Creates a full blog post with its own page

---

### 4. Teaching / Courses

**Location:** `_data/teaching.yml`

#### Adding a Course

```yaml
- title: "E9 213 Time-Frequency Analysis"
  description: "Course description here..."
  instructor: "Prof. Chandra Sekhar Seelamantula"
  teaching_assistants: ["TA Name 1", "TA Name 2"]
  semester: "Aug. 2025"
  permalink: "/teaching/e9-213-time-frequency-analysis/"
  course_id: "e9-213"
  type: "Regular Course"           # or "Short Course"
```

**For Short Courses (with external instructor):**

```yaml
- title: "Special Topic Course"
  description: "Course description..."
  instructor: "Prof. External Name"
  instructor_bio: "Brief bio of the instructor..."
  instructor_photo: "assets/img/people/instructors/name.jpg"
  hosts: ["Prof. C. S. Seelamantula", "Prof. Another Host"]
  teaching_assistants: ["TA 1", "TA 2"]
  semester: "Dec. 2025"
  permalink: "/teaching/special-topic/"
  course_id: "st"
  type: "Short Course"
```

---

### 5. Recognition & Awards

**Location:** `_data/recognition.yml`

#### Adding an Award

```yaml
- name: "Student Name"
  award: "Award Title"
  year: "2025"
  category: "Award"
  image: "assets/img/recognition/award-photo.jpg"   # Optional
```

**Image location:** `assets/img/recognition/`

---

### 6. Funding / Sponsors

**Location:** `_data/funding.yml`

#### Adding a Funder

```yaml
- logo: /assets/img/funders/organization-logo.png
  url: https://organization-website.com
  name: "Organization Name"
  invert: false                 # true if logo needs color inversion in dark mode
```

**Logo requirements:**
- Location: `assets/img/funders/`
- Format: PNG, SVG, or JPG
- Recommended: Transparent background PNG

**Dark mode handling:**
- Set `invert: true` for dark logos that need to be inverted in dark mode
- Logos automatically display in a grayscale carousel with color on hover

---

### 7. Professional Activities (Lab Director)

**Location:** `_data/activities.yml`

This file contains the Lab Director's professional activities shown on their profile page.

#### Structure:

```yaml
# Invited talks delivered
talks_delivered:
  - title: "Talk Title"
    venue: "Conference/Institution Name"
    date: "Month Day, Year"
    type: "Keynote"              # Workshop, Conference, Tutorial, etc.
    note: "Additional info"      # Optional

# Invited talks organized
talks_organized:
  - title: "Talk Title"
    speaker: "Speaker Name"
    speaker_affiliation: "Speaker's Institution"
    date: "Month Day, Year"
    note: "Additional info"      # Optional

# Committee memberships
committees:
  current_roles:
    - title: "Role Title"
      organization: "Organization"
      period: "2023-Present"
      type: "Committee"
  
  editorial_service:
    - title: "Associate Editor"
      organization: "Journal Name"
      period: "2020-2024"
      type: "Editorial"
  
  conference_organization:
    - title: "General Chair"
      organization: "Conference Name"
      period: "2025"
      location: "City, Country"
      type: "Conference Leadership"
  
  academic_service:
    - title: "Committee Member"
      organization: "Institution"
      period: "2022-2023"
      type: "Academic Administration"
```

---

### 8. Projects

**Location:** `_projects/`

#### Adding a Project

Create a markdown file (e.g., `_projects/project-name.md`):

```yaml
---
layout: page
title: Project Title
description: Brief description for the card
img: assets/img/projects/project-image.jpg
importance: 1                    # Lower = appears first
category: work                   # Category for filtering
related_publications: true       # Show related papers
---

Full project description in Markdown...

## Overview

Project details here...

## Results

Include images:
{% include figure.liquid path="assets/img/projects/result.jpg" title="Result" class="img-fluid rounded" %}
```

---

### 9. Photo Album

**Location:** 
- Data: `_data/album.yaml`
- Images: `assets/img/album/[category]/`

#### Adding Album Categories

Edit `_data/album.yaml`:

```yaml
- title: "Lab Events"
  folder: "lab-events"           # Matches folder in assets/img/album/
  description: "Photos from lab events and celebrations"
```

#### Adding Photos

1. Create folder: `assets/img/album/[folder-name]/`
2. Add images numbered sequentially: `1.jpg`, `2.jpg`, etc.

---

## 🖼️ Adding Images

### Image Locations

| Type | Location |
|------|----------|
| Profile photos | `assets/img/people/[category]/` |
| Funder logos | `assets/img/funders/` |
| Award photos | `assets/img/recognition/` |
| Album photos | `assets/img/album/[category]/` |
| Project images | `assets/img/projects/` |
| Research highlights | `assets/img/research-highlights/` |
| Logos | `assets/img/logo/` |

### Image Guidelines

- **Profile photos:** Square aspect ratio, minimum 400x400px
- **Logos:** PNG with transparent background preferred
- **General images:** JPG or PNG, reasonable file size (< 500KB)
- **Supported formats:** JPG, PNG, WebP, SVG

### Automatic Processing

The site uses ImageMagick to automatically generate responsive image sizes (480px, 800px, 1400px widths) during build.

---

## 🌙 Dark Mode Support

The site supports automatic dark/light mode switching. When adding content:

1. **Logos with dark backgrounds:** Set `invert: true` in `funding.yml`
2. **Custom images:** Use CSS variables for colors that need to adapt
3. **Bootstrap classes:** The site overrides `.bg-light`, `.text-dark`, etc. for dark mode

---

## 🛠️ Development

### File Formatting

Format Liquid/HTML/Markdown files:

```bash
npx prettier --plugin=@shopify/prettier-plugin-liquid --write "**/*.{liquid,md,html}"
```

### Building for Production

```bash
JEKYLL_ENV=production bundle exec jekyll build
```

The built site will be in `_site/`.

### Key Configuration

Main configuration is in `_config.yml`:

```yaml
title: Spectrum Lab
email: css@iisc.ac.in
url: "https://spectrum-lab-iisc.github.io"
```

---

## 🚢 Deployment

The site automatically deploys to GitHub Pages when changes are pushed to the `main` branch.

### Manual Deployment Steps

1. Make changes locally
2. Test with local server
3. Commit and push to `main`
4. GitHub Actions builds and deploys automatically
5. Changes appear at https://spectrum-lab-iisc.github.io within minutes

---

## 🔧 Troubleshooting

### Common Issues

**Build fails with SCSS error:**
- Check for syntax errors in `_sass/` files
- Ensure all variables are defined

**Images not showing:**
- Verify file path matches exactly (case-sensitive)
- Check file exists in the correct location
- For responsive images, ensure ImageMagick is installed

**Person not appearing:**
- Ensure `show: true` in front matter
- Check file is in correct category folder
- Verify YAML syntax is correct

**Publications not showing:**
- Validate BibTeX syntax
- Ensure required fields are present
- Check for special characters that need escaping

### Validating Changes

```bash
# Build and check for errors
bundle exec jekyll build --verbose

# Serve and check console for errors
bundle exec jekyll serve --livereload --port 8080
```

---

## 📚 Technology Stack

- **[Jekyll](https://jekyllrb.com/)** - Static site generator
- **[al-folio](https://github.com/alshedivat/al-folio)** - Academic theme (customized)
- **[Bootstrap 5](https://getbootstrap.com/)** - CSS framework
- **[ImageMagick](https://imagemagick.org/)** - Image processing
- **[jekyll-scholar](https://github.com/inukshuk/jekyll-scholar)** - BibTeX processing
- **[GitHub Pages](https://pages.github.com/)** - Hosting


---

**Maintained by Spectrum Lab, IISc Bengaluru**
