# 🌊 Spectrum Lab Website

Official website for **Spectrum Lab** at the Department of Electrical Engineering, Indian Institute of Science (IISc), Bengaluru.

🌐 **Live Site:** [spectrum.ee.iisc.ac.in](https://spectrum.ee.iisc.ac.in)

---

## 📖 Table of Contents

- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [How to Update Content](#-how-to-update-content)
  - [People / Team Members](#1-people--team-members)
  - [Publications](#2-publications)
  - [News & Announcements](#3-news--announcements)
  - [Projects](#4-projects)
  - [Data Files (Funding, Awards, Teaching)](#5-data-files)
- [Image Optimization (CRITICAL)](#-image-optimization-critical)
- [Styling & Dark Mode](#-styling--dark-mode)
- [Configuration](#-configuration)
- [Deployment](#-deployment)

---

## 🚀 Quick Start

### Prerequisites
- Ruby 3.x
- Bundler (`gem install bundler`)
- ImageMagick (Required for image optimization)

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

### Using Docker

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
│   ├── emails.yml          # Email aliases for bibliography
│   ├── funding.yml         # Funding sources/sponsors
│   ├── recognition.yml     # Awards and recognition
│   ├── teaching.yml        # Course listings
│   └── ...
├── _includes/              # Reusable HTML/Liquid components
│   ├── responsive-image.liquid  # ⭐ MAIN IMAGE INCLUDE
│   └── ...
├── _layouts/               # Page templates
├── _news/                  # News announcements
├── _pages/                 # Static pages (about, etc.)
├── _people/                # Team member profiles
│   ├── current/            # Active members (phd, mtech, etc.)
│   └── alumni/             # Former members
├── _projects/              # Research project pages
├── _sass/                  # SCSS stylesheets
├── assets/
│   └── img/                # All images (people, projects, etc.)
└── _config.yml             # Site configuration
```

---

## 📝 How to Update Content

### 1. People / Team Members

**Location:** `_people/`

**Structure:**
- `current/` - Active lab members (subfolders: `phd-students`, `mtech-students`, etc.)
- `alumni/` - Former members (subfolders: `phd-graduates`, etc.)

#### Adding a New Person

1. **Copy the template:**
   ```bash
   cp _people/person_template.md _people/current/phd-students/firstname-lastname.md
   ```

2. **Add their photo:**
   - Save to `assets/img/people/[category]/filename.jpg`
   - **Requirement:** Square aspect ratio, min 400x400px.

3. **Edit the markdown file:**
   Update `title`, `firstname`, `lastname`, `img` path, and `category`.

#### Moving to Alumni
Move the file from `current/[category]/` to `alumni/[category-graduates]/`.

---

### 2. Publications

**Location:** `_bibliography/papers.bib`

1. **Add BibTeX entry:**
   ```bibtex
   @article{key2025,
     author = {Author, A. and Seelamantula, C. S.},
     title = {Paper Title},
     year = {2025},
     preview = {thumbnail.png},  # Optional: Image in assets/img/publication_preview/
     emails = {alias1, css},     # Use aliases from _data/emails.yml
     bibtex_show = {true},
     selected = {true}           # Show on homepage
   }
   ```

2. **Manage Authors:**
   - Use **aliases** in the `emails` field to link authors to their profile pages.
   - Define new aliases in `_data/emails.yml`.

---

### 3. News & Announcements

**Location:** `_news/`

Create a file `YYYY-MM-DD-title.md`:

```yaml
---
layout: post
title: "News Title"
date: 2025-01-15
inline: true   # true = one-line announcement, false = full blog post
---
Announcement text here...
```

---

### 4. Projects

**Location:** `_projects/`

Create a markdown file (e.g., `project-name.md`):

```yaml
---
layout: page
title: Project Title
description: Short description
img: assets/img/projects/image.jpg
importance: 1
category: work
---
Full project description...
```

---

### 5. Data Files

| File | Purpose |
|------|---------|
| `_data/funding.yml` | Sponsors shown in the homepage carousel. |
| `_data/recognition.yml` | Awards and honors list. |
| `_data/teaching.yml` | Courses taught by the lab director. |
| `_data/activities.yml` | Professional activities (talks, committees). |
| `_data/album.yaml` | Categories for the photo album. |

---

## 🖼️ Image Optimization (CRITICAL)

The site uses **ImageMagick** to automatically generate optimized WebP images.

**❌ NEVER use raw HTML `<img>` tags.**

**✅ ALWAYS use the provided Liquid includes:**

1.  **Standard Image (Responsive):**
    ```liquid
    {% include responsive-image.liquid path="assets/img/photo.jpg" alt="Alt text" class="img-fluid" %}
    ```

2.  **Figure with Caption:**
    ```liquid
    {% include figure.liquid path="assets/img/photo.jpg" title="Caption" class="img-fluid" %}
    ```

3.  **Simple/Small Image (Logos):**
    ```liquid
    {% include simple-image.liquid path="assets/img/logo.png" alt="Logo" %}
    ```

**Note:** New images are processed during the build. Ensure ImageMagick is installed locally.

---

## 🎨 Styling & Dark Mode

- **SCSS Location:** `_sass/`
- **Dark Mode:** The site supports automatic dark mode.
  - Use CSS variables (`var(--global-bg-color)`) instead of hardcoded colors.
  - For logos in `funding.yml`, set `invert: true` if they need to be inverted in dark mode.

---

## ⚙️ Configuration

- **Main Config:** `_config.yml` (Site title, URL, analytics, etc.)
- **Typography:** `_data/typography.yml` (Font families, sizes, math engine settings).

---

## ship: Deployment

The site is hosted on **GitHub Pages**.
- **Automatic:** Pushing to `main` triggers a GitHub Action to build and deploy.
- **Manual Check:** Always run `JEKYLL_ENV=production bundle exec jekyll build` locally before pushing to catch errors.

---

**Maintained by Spectrum Lab, IISc Bengaluru**
