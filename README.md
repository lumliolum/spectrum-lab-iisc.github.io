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
  - [Data Files](#5-data-files)
  - [Recognition / Awards](#6-recognition--awards)
  - [Talks](#7-talks)
  - [Articles (Research Highlights)](#8-articles-research-highlights)
- [Image Optimization (CRITICAL)](#-image-optimization-critical)
- [Typography & Math Rendering](#-typography--math-rendering)
- [Styling & Dark Mode](#-styling--dark-mode)
- [Utility Scripts](#-utility-scripts)
- [Configuration](#-configuration)
- [Deployment](#-deployment)

---

## 🚀 Quick Start

### Prerequisites
- Ruby 3.x
- Bundler (`gem install bundler`)
- ImageMagick (Required for image optimization)
- Python 3.x (For utility scripts)

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
├── _articles/              # Research highlight articles (distill-style)
├── _bibliography/          # BibTeX publications
│   └── papers.bib          # All publications go here
├── _data/                  # YAML data files
│   ├── activities.yml      # Lab Director's professional activities
│   ├── album.yaml          # Photo album categories
│   ├── coauthors.yml       # Co-author highlighting
│   ├── contacts.yml        # Contact information
│   ├── funding.yml         # Funding sources/sponsors
│   ├── recognition.yml     # Awards and honors
│   ├── teaching.yml        # Course listings
│   ├── typography.yml      # Fonts & math engine settings
│   ├── venues.yml          # Publication venues
│   └── videos.yml          # Video gallery entries
├── _includes/              # Reusable HTML/Liquid components
│   ├── responsive-image.liquid  # ⭐ Primary image include
│   ├── figure.liquid            # Image with caption
│   ├── simple-image.liquid      # Simple optimized image
│   └── ...
├── _layouts/               # Page templates
├── _news/                  # News announcements (organized by year)
├── _pages/                 # Static pages
├── _people/                # Team member profiles
│   ├── current/            # Active members
│   │   ├── administrator/
│   │   ├── interns/
│   │   ├── lab-director/
│   │   ├── mtech-research/
│   │   ├── mtech-students/
│   │   ├── phd-students/
│   │   └── project-associates/
│   └── alumni/             # Former members
│       ├── interns/
│       ├── mtech-graduates/
│       ├── mtech-research-graduates/
│       ├── phd-graduates/
│       ├── post-doc/
│       └── research-associates/
├── _talks/                 # Talk/presentation archives
│   ├── delivered/          # Talks given (by year)
│   └── organized/          # Events organized
├── _sass/                  # SCSS stylesheets
│   ├── _base.scss          # Core styles, design tokens
│   ├── _themes.scss        # Light/dark theme variables
│   └── _person.scss        # Person page styles
├── assets/
│   └── img/                # All images
├── scripts/                # Utility scripts
└── _config.yml             # Site configuration
```

---

## 📝 How to Update Content

### 1. People / Team Members

**Location:** `_people/`

**Structure:**
- `current/` - Active lab members (subfolders: `phd-students`, `mtech-students`, `interns`, `project-associates`, etc.)
- `alumni/` - Former members (subfolders: `phd-graduates`, `mtech-graduates`, `post-doc`, etc.)

#### Adding a New Person

1. **Create a new file** in the appropriate subfolder:
   ```bash
   # Example for a PhD student
   touch _people/current/phd-students/firstname-lastname.md
   ```

2. **Add their photo:**
   - Save to `assets/img/people/current/[category]/filename.jpg`
   - **Requirement:** Square aspect ratio recommended, min 400x400px.

3. **Edit the markdown file** with the following front-matter:

   ```yaml
   ---
   layout: person
   title: Full Name
   firstname: First
   lastname: Last
   description: PhD Student
   img: assets/img/people/current/phd-students/filename.jpg
   category: PhD Students
   show: true
   
   # Contact & Links
   email: name@iisc.ac.in
   alias: firstname_or_unique_id   # Used for linking publications & awards
   website: https://personal-site.com
   linkedin_username: username
   github_username: username
   scholar_userid: GOOGLE_SCHOLAR_ID
   
   # Optional
   fellowship: "Fellowship Name"
   
   biography_paragraphs:
     - "First paragraph of biography..."
     - "Second paragraph..."
   ---
   ```

#### Key Fields

| Field | Description |
|-------|-------------|
| `alias` | **Unique identifier** for linking to publications (`emails` field in BibTeX) and awards |
| `email` | Contact email |
| `category` | Display category: "PhD Students", "MTech Students", "PhD Graduates", etc. |
| `show` | Set to `true` to display on the website |
| `scholar_userid` | Google Scholar ID for automatic publication listing |


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
     emails = {alias1, css},     # Use person aliases to link to profiles
     bibtex_show = {true},
     selected = {true}           # Show on homepage
   }
   ```

2. **Link Authors to Profiles:**
   - Use person **aliases** in the `emails` field
   - Aliases are defined in each person's markdown file (`alias: firstname`)
   - This enables automatic linking between publications and person profiles

---

### 3. News & Announcements

**Location:** `_news/[YEAR]/`

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

### 5. Data Files

| File | Purpose |
|------|---------|
| `_data/funding.yml` | Sponsors shown in the homepage carousel |
| `_data/recognition.yml` | Awards, patents, and honors |
| `_data/teaching.yml` | Courses taught |
| `_data/activities.yml` | Professional activities (talks, committees) |
| `_data/album.yaml` | Photo album event categories |
| `_data/videos.yml` | Video gallery entries |
| `_data/typography.yml` | Site-wide typography and math settings |
| `_data/coauthors.yml` | Co-author name highlighting |
---

### 6. Recognition / Awards

**Location:** `_data/recognition.yml`

Awards are centrally managed and displayed on the Recognition page and linked person profiles.

#### Adding a New Award

```yaml
awards:
  - award: "Award Name"
    year: "2024"
    category: "Award"
    recipients: "Full Name 1, Full Name 2"  # Comma-separated names
    image: "assets/img/recognition/folder/image.jpg"
```

#### Key Fields

| Field | Description |
|-------|-------------|
| `award` | Name of the award |
| `year` | Year(s) received (can be comma-separated: "2019, 2021, 2022") |
| `category` | "Award", "Patent", "Honor" |
| `recipients` | **Comma-separated full names** of recipients |
| `image` | Path to award image (optional) |
| `images` | Array of images with captions for carousel (optional) |

#### Image Organization

Images are organized by person or category in `assets/img/recognition/`:
```
assets/img/recognition/
├── siddarth/          # Person-specific award images
├── qualcomm/          # Group awards (Qualcomm fellowships)
├── css/               # Lab Director's awards
└── ...
```

---

### 7. Talks

**Location:** `_talks/`

**Structure:**
- `delivered/[YEAR]/` - Talks given by lab members
- `organized/` - Events/workshops organized

#### Adding a New Talk

Create a file `YYYY-MM-DD-talk-title.md` in the appropriate folder:

```yaml
---
layout: talk
title: "Talk Title"
date: 2024-10-10
time: "3:30 PM"
venue: "Venue Name"
type: "Talk"
category: delivered
speaker: "Prof. Chandra Sekhar Seelamantula"
speaker_affiliation: "Department of Electrical Engineering, IISc"
host: "Dr. Host Name"
keywords:
  - keyword1
  - keyword2
abstract: |
  Multi-line abstract text here...
speaker_bio: |
  Speaker biography...
---
```

---

### 8. Articles (Research Highlights)

**Location:** `_articles/`

Research highlight articles use the distill-style layout with interactive features.

#### Creating a New Article

```yaml
---
layout: distill
title: "Article Title"
description: "Brief description"
date: 2024-04-18
post_author: Author Name
authors:
  - name: Author Name
    url: "https://author-website.com"
    affiliations:
      name: Institution
paper_url: https://link-to-paper.com
doi: 10.xxxx/xxxxx
bibliography: article-bibliography.bib
thumbnail: assets/img/research-highlights/thumbnail.jpg
toc: true
related_posts: true

# Math Configuration (optional - uses defaults from typography.yml)
# math_engine: mathjax    # "mathjax", "katex", or false
# math_font: mathjax-modern
---

Article content with LaTeX math support: $$E = mc^2$$
```

---

## 🖼️ Image Optimization (CRITICAL)

The site uses **ImageMagick** to automatically generate optimized WebP images at multiple sizes (480w, 800w, 1400w).

**❌ NEVER use raw HTML `<img>` tags.**

**✅ ALWAYS use the provided Liquid includes:**

1.  **Responsive Image (Primary - for most images):**
    ```liquid
    {% include responsive-image.liquid path="assets/img/photo.jpg" alt="Alt text" class="img-fluid" %}
    ```

2.  **Figure with Caption:**
    ```liquid
    {% include figure.liquid path="assets/img/photo.jpg" alt="Alt text" caption="Caption text" class="img-fluid" %}
    ```

3.  **Simple Image (for logos, icons):**
    ```liquid
    {% include simple-image.liquid path="assets/img/logo.png" alt="Logo" %}
    ```

**Note:** New images are processed during build. Ensure ImageMagick is installed locally.

---

## 🔤 Typography & Math Rendering

**Configuration:** `_data/typography.yml`

### Typography System
- Centralized font configuration for body, headings, code, and serif text
- CSS variables generated site-wide via `_includes/typography-styles.liquid`
- Google Fonts and Adobe Fonts (Typekit) support

### Math Rendering
- **Default engine:** MathJax (configurable)
- **Inline math:** `$E = mc^2$` or `\(E = mc^2\)`
- **Display math:** `$$\int_0^\infty f(x)dx$$` or `\[\int_0^\infty f(x)dx\]`

#### Per-Article Math Override
Articles can override global math settings in front-matter:
```yaml
math_engine: mathjax    # Options: "mathjax", "katex", or false
math_font: mathjax-modern  # MathJax fonts: mathjax-modern, mathjax-stix2, etc.
```

**Available MathJax fonts:** `mathjax-modern`, `mathjax-stix2`, `mathjax-termes`, `mathjax-pagella`, `mathjax-gyre`, `mathjax-fira`

---

## 🎨 Styling & Dark Mode

- **SCSS Location:** `_sass/`
- **Key Files:**
  - `_base.scss` — Core styles, design tokens, dark mode fixes
  - `_themes.scss` — Light/dark theme CSS variables
  - `_person.scss` — Person profile page styles

### Design Tokens (in `_base.scss`)
```scss
$spacing-xs: 0.25rem;  $spacing-sm: 0.5rem;   $spacing-md: 1rem;
$spacing-lg: 1.5rem;   $spacing-xl: 2rem;     $spacing-2xl: 3rem;
$radius-sm: 4px;       $radius-md: 8px;       $radius-lg: 12px;
$transition-fast: 150ms ease;  $transition-normal: 250ms ease;
```

### Dark Mode Guidelines
- Use CSS variables (`var(--global-bg-color)`) instead of hardcoded colors
- For funding logos, set `invert: true` in `funding.yml` if they need inversion in dark mode
- Test both themes when making style changes

---

## 🔧 Utility Scripts

**Location:** `scripts/`

| Script | Purpose |
|--------|---------|
| `ensure_person_fields.py` | Auto-fills missing `email` and `alias` fields in person profiles |
| `process_photos.py` | Batch process and optimize photos |
| `fetch_scholar.py` | Fetch publication data from Google Scholar |
| `generate_coauthors.rb` | Generate co-author YAML from BibTeX |
| `extract_pdf_text.py` | Extract text from PDF files |
| `download_from_google.py` | Download files from Google Drive |

Run scripts from the project root:
```bash
python3 scripts/ensure_person_fields.py
```

---

## ⚙️ Configuration

| File | Purpose |
|------|---------|
| `_config.yml` | Site title, URL, plugins, analytics, ImageMagick settings |
| `_data/typography.yml` | Font families, sizes, math engine configuration |
| `_data/contacts.yml` | Contact information |

---

## 🚀 Deployment

The site is hosted on **GitHub Pages**.

- **Automatic:** Pushing to `main` triggers a GitHub Action to build and deploy
- **Production Build:** Always run locally before pushing to catch errors:
  ```bash
  JEKYLL_ENV=production bundle exec jekyll build
  ```

---

## 🔍 Files to Check First

| Task | Check These Files |
|------|-------------------|
| Person display issues | `_includes/people.liquid`, `_layouts/person.liquid`, `_sass/_person.scss` |
| Image problems | `_includes/responsive-image.liquid`, `_includes/figure.liquid`, `_config.yml` |
| Dark mode bugs | `_sass/_base.scss`, `_sass/_themes.scss` |
| Homepage content | `_pages/about.md`, `_includes/funding.liquid`, `_includes/news.liquid` |
| Navigation | `_includes/components/navbar.liquid`, `_includes/header.liquid` |
| Publications | `_bibliography/papers.bib`, `_layouts/bib.liquid` |
| Typography/Fonts | `_data/typography.yml`, `_includes/typography-styles.liquid` |
| Math rendering | `_data/typography.yml`, `_includes/scripts/mathjax.liquid` |
| Talks | `_talks/`, `_layouts/talk.liquid` |
| Articles | `_articles/`, `_layouts/distill.liquid` |

---

**Maintained by Spectrum Lab, IISc Bengaluru**
