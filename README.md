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

# Ensure all person profiles have required fields (optional, auto-fills missing email/alias)
python3 scripts/ensure_person_fields.py

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
│   ├── funding.yml         # Funding sources/sponsors
│   ├── recognition.yml     # Awards and recognition (uses aliases)
│   ├── teaching.yml        # Course listings
│   └── ...
├── _includes/              # Reusable HTML/Liquid components
│   ├── responsive-image.liquid  # ⭐ MAIN IMAGE INCLUDE
│   └── ...
├── _layouts/               # Page templates
├── _news/                  # News announcements
├── _pages/                 # Static pages (about, etc.)
├── _people/                # Team member profiles
│   ├── current/            # Active members (subfolders: phd-students, mtech-students/2026/, etc.)
│   └── alumni/             # Former members (subfolders: phd-graduates/2024/, etc.)
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
- `current/` - Active lab members (subfolders: `phd-students`, `mtech-students/2026/`, etc.)
- `alumni/` - Former members (subfolders: `phd-graduates/2024/`, etc.)

#### Adding a New Person

1. **Copy the template:**
   ```bash
   cp _people/person_template.md _people/current/phd-students/firstname-lastname.md
   ```

2. **Add their photo:**
   - Save to `assets/img/people/[category]/filename.jpg`
   - **Requirement:** Square aspect ratio, min 400x400px.

3. **Edit the markdown file:**
   Update `title`, `firstname`, `lastname`, `img` path, `category`, `year`, and importantly:

   **`alias`** - Used for linking to publications and awards:
   ```yaml
   alias: siddarth  # Must match aliases in papers.bib and recognition.yml
   ```

#### Key Fields

| Field | Description |
|-------|-------------|
| `alias` | **Unique identifier** for bibliography and recognition lookups |
| `email` | Contact email (also used in emails.yml) |
| `category` | "PhD Graduates", "MTech Graduates", etc. |
| `year` | Graduation year |


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
     emails = {alias1, css},     # Use aliases from person profiles
     bibtex_show = {true},
     selected = {true}           # Show on homepage
   }
   ```

2. **Manage Authors:**
   - Use **aliases** in the `emails` field to link authors to their profile pages.
   - Aliases are defined in individual person markdown files (e.g., `alias: siddarth`).

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
| `_data/recognition.yml` | Awards and honors (linked via person aliases). |
| `_data/teaching.yml` | Courses taught by the lab director. |
| `_data/activities.yml` | Professional activities (talks, committees). |
| `_data/album.yaml` | Categories for the photo album. |

---

### 6. Recognition / Awards

**Location:** `_data/recognition.yml`

Awards are centrally managed and automatically displayed on person profile pages via their `alias` field.

#### Adding a New Award

```yaml
- award: "Award Name"
  year: "2024"
  category: "Award"
  aliases: "siddarth, nishanths"  # Comma-separated aliases from person profiles
  image: "assets/img/recognition/folder/image.jpg"
```

#### Key Fields

| Field | Description |
|-------|-------------|
| `award` | Name of the award |
| `year` | Year(s) received (can be comma-separated: "2019, 2021, 2022") |
| `aliases` | **Comma-separated aliases** matching `alias` field in person profiles |
| `image` | Path to award image (optional) |
| `images` | Array of images with captions for carousel (optional) |
| `co_inventors` | For joint awards with external collaborators |

#### How It Works

1. **Aliases** are defined in each person's markdown file:
   ```yaml
   alias: siddarth  # In the person's profile
   ```

2. **Awards reference aliases**:
   ```yaml
   - award: "Qualcomm Innovation Fellowship"
     aliases: "nishanths, nareddyreddy"  # Both people get this award
   ```

3. **Person profiles automatically show awards:**
   - The layout matches person's alias → recognition entries
   - No need to edit individual markdown files

#### Image Organization

Images are organized by person in `assets/img/recognition/`:
```
assets/img/recognition/
├── siddarth/          # All Siddarth's award images
├── qualcomm/          # Group awards (Qualcomm fellowships)
├── css/               # Lab Director's awards
└── ...
```

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
