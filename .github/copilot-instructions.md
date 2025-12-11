# Copilot / AI Agent Instructions — Spectrum Lab Website

This repo is a Jekyll-based academic website (al-folio theme) for **Spectrum Lab at IISc Bengaluru**, hosted on GitHub Pages. This guide provides repository-specific structure, developer workflows, and conventions for AI coding agents.

---

## Project Overview

- **Stack:** Jekyll 4.x + al-folio theme + Bootstrap + SCSS
- **Content Sources:** Markdown files in `_pages`, `_posts`, `_people`, `_projects`, `_articles`, `_news`
- **Data Files:** YAML in `_data/` (funding.yml, recognition.yml, teaching.yml, activities.yml, album.yaml, etc.)
- **Bibliography:** BibTeX in `_bibliography/papers.bib` (jekyll-scholar plugin)
- **Styling:** SCSS in `_sass/` — key files: `_base.scss`, `_themes.scss`, `_person.scss`, `_funding.scss`
- **Templates:** Liquid templates in `_layouts/` and `_includes/`
- **Assets:** Static files under `assets/` (images, CSS, JS)

---

## Local Development

```bash
# Install dependencies
bundle install

# Serve with live reload (development)
JEKYLL_ENV=development bundle exec jekyll serve --livereload --port 8080

# Build for production
JEKYLL_ENV=production bundle exec jekyll build

# Docker development
docker-compose up --build
```

---

## Image Optimization (CRITICAL)

**All images are processed by ImageMagick and converted to optimized WebP format.**

### Configuration (`_config.yml`):
- Input formats: `.jpg`, `.jpeg`, `.png`, `.tiff`, `.tif`, `.gif`, `.bmp`, `.webp` (case-insensitive)
- Output: WebP at 480px, 800px, 1400px widths
- Quality: 80 with `-strip -define webp:method=6`

### Image Includes (use these, never raw `<img>` tags):
1. **`responsive-image.liquid`** — Best for content images, people photos, album
   - Outputs `<picture>` with WebP srcset at 480w/800w/1400w
   - Default src is WebP with onerror fallback to original
   ```liquid
   {% include responsive-image.liquid path="assets/img/photo.jpg" alt="Description" class="img-fluid" %}
   ```

2. **`figure.liquid`** — For images with captions, zoomable images
   - Wraps in `<figure>` element
   - Supports captions, zoomable, custom sizes
   ```liquid
   {% include figure.liquid path="assets/img/photo.jpg" alt="Description" caption="Caption text" class="img-fluid" %}
   ```

3. **`simple-image.liquid`** — For logos, icons, simple images
   - Lightweight, single WebP with fallback
   ```liquid
   {% include simple-image.liquid path="assets/img/logo.png" alt="Logo" class="navbar-logo" %}
   ```

### NEVER do this:
```html
<!-- BAD: Direct img tag bypasses optimization -->
<img src="{{ image | relative_url }}" alt="...">
```

---

## Key Directory Structure

```
_people/           # Person profiles (one .md file per person)
  ├── lab-director/
  ├── phd-students/
  ├── mtech-students/
  ├── mtech-research/
  ├── project-associates/
  ├── phd-graduates/
  └── mtech-research-graduates/

_data/             # YAML data files
  ├── funding.yml      # Funding sources (carousel on homepage)
  ├── recognition.yml  # Awards, patents, honors
  ├── teaching.yml     # Course information
  ├── activities.yml   # Professional activities (Lab Director)
  ├── album.yaml       # Photo album events
  └── coauthors.yml    # Co-author highlighting

_layouts/          # Page layouts
  ├── default.liquid   # Base layout (includes head, navbar, footer)
  ├── person.liquid    # Individual person profile page
  ├── recognition.liquid
  ├── album.liquid
  └── bib.liquid       # Bibliography entry

_includes/         # Reusable components
  ├── responsive-image.liquid  # ⭐ Primary image include
  ├── figure.liquid            # Image with caption
  ├── simple-image.liquid      # Simple optimized image
  ├── people.liquid            # Person card component
  ├── funding.liquid           # Funding carousel (Swiper)
  ├── news.liquid              # News list
  ├── recognition.liquid       # Awards display
  └── components/
      ├── navbar.liquid
      ├── footer.liquid
      └── theme-toggle.liquid

_sass/             # SCSS stylesheets
  ├── _base.scss       # Core styles, design tokens, dark mode fixes
  ├── _themes.scss     # Light/dark theme variables
  ├── _person.scss     # Person page styles, nested accordions
  └── _funding.scss    # Funding carousel styles
```

---

## Adding Content

### Add a New Person
1. Copy `_people/person_template.md` to appropriate subfolder
2. Fill front-matter fields:
   ```yaml
   layout: person
   title: Full Name
   firstname: First
   lastname: Last
   description: PhD Student
   img: assets/img/people/phd/filename.jpg  # Will be converted to WebP
   category: PhD Students
   show: true
   email: name@iisc.ac.in
   scholar_userid: XXXXX  # For publications
   ```
3. Add photo to `assets/img/people/[category]/`

### Add a Publication
1. Add BibTeX entry to `_bibliography/papers.bib`
2. Include `preview` field for thumbnail: `preview = {thumbnail.png}`
3. Preview images go in `assets/img/publication_preview/`

### Add News
Create file in `_news/` with front-matter:
```yaml
---
layout: post
title: News Title
date: 2025-01-15
inline: true  # For short announcements
---
```

### Add Recognition/Award
Add to `_data/recognition.yml`:
```yaml
- name: Recipient Name
  award: Award Description
  year: "2025"
  category: Award  # or Patent, Honor
  image: assets/img/recognition/photo.jpg  # Optional
  url: https://...  # Optional link
```

### Add Funding Source
Add to `_data/funding.yml`:
```yaml
- name: Funder Name
  logo: assets/img/funding/logo.png
  url: https://funder-website.com
  invert: false  # true if logo needs inversion in dark mode
```

---

## Styling Conventions

### Design Tokens (in `_base.scss`)
```scss
$spacing-xs: 0.25rem;
$spacing-sm: 0.5rem;
$spacing-md: 1rem;
$spacing-lg: 1.5rem;
$spacing-xl: 2rem;
$spacing-2xl: 3rem;
$spacing-3xl: 4rem;

$radius-sm: 4px;
$radius-md: 8px;
$radius-lg: 12px;

$transition-fast: 150ms ease;
$transition-normal: 250ms ease;
```

### Dark Mode
- Uses CSS custom properties (`--global-*`)
- Theme toggle in navbar
- All components must support both themes
- Bootstrap utility overrides in `_base.scss` for dark mode compatibility

### Typography System
- Central config: `_data/typography.yml` — controls all fonts site-wide
- CSS variables generated by `_includes/typography-styles.liquid`
- Body, heading, code, and serif font families configurable
- Font weights and sizes defined in YAML, applied via CSS custom properties

### Math Rendering
- Default engine: MathJax (configurable in `_data/typography.yml`)
- Per-article override via frontmatter:
  ```yaml
  math_engine: mathjax  # or katex, or false to disable
  math_font: mathjax-stix2  # or mathjax-modern, etc.
  enable_math: true
  ```
- Available MathJax fonts: `mathjax-modern`, `mathjax-stix2`, `mathjax-termes`, `mathjax-pagella`
- Math loader: `_includes/scripts/mathjax.liquid`

### Key CSS Classes
- `.spectrum-logo-light` / `.spectrum-logo-dark` — Logo variants
- `.funding-logo-invert` — Invert funding logos in dark mode
- `.nested-accordion` — Collapsible sections (used in person.liquid)

---

## Common Tasks

### Fix Image Not Loading
1. Check path is correct in front-matter/template
2. Ensure using `responsive-image.liquid`, `figure.liquid`, or `simple-image.liquid`
3. Verify image exists in `assets/img/`
4. Run build to generate WebP versions

### Fix Dark Mode Issue
1. Check element uses CSS custom properties (`var(--global-*)`)
2. Add override in `html[data-theme="dark"]` block in `_base.scss`
3. For Bootstrap utilities, add explicit dark mode override

### Add New Component
1. Create `_includes/components/component-name.liquid`
2. Add styles to appropriate SCSS file
3. Include dark mode support
4. Use existing design tokens

---

## Build & Deploy

- **GitHub Pages:** Auto-deploys on push to `main`
- **Local testing:** Always test with `JEKYLL_ENV=production bundle exec jekyll build`
- **ImageMagick required:** Install locally or use Docker for image processing

---

## Gotchas & Tips

1. **Image optimization:** Always use the include templates, never raw `<img>` tags
2. **WebP generation:** Happens at build time; new images need a rebuild
3. **Dark mode:** Test both themes when making style changes
4. **Swiper.js:** Used for funding carousel; CSS loaded via CDN
5. **jekyll-scholar:** Publications are BibTeX-driven; check `papers.bib` syntax
6. **Person categories:** Must match folder names in `_people/` and category values

---

## Files to Check First

| Task | Check These Files |
|------|-------------------|
| Person display issues | `_includes/people.liquid`, `_layouts/person.liquid`, `_sass/_person.scss` |
| Image problems | `_includes/responsive-image.liquid`, `_includes/figure.liquid`, `_config.yml` (imagemagick section) |
| Dark mode bugs | `_sass/_base.scss`, `_sass/_themes.scss` |
| Homepage content | `_pages/about.md`, `_includes/funding.liquid`, `_includes/news.liquid` |
| Navigation | `_includes/components/navbar.liquid`, `_includes/header.liquid` |
| Publications | `_bibliography/papers.bib`, `_layouts/bib.liquid` |
| Typography/Fonts | `_data/typography.yml`, `_includes/typography-styles.liquid` |
| Math rendering | `_data/typography.yml` (math section), `_includes/scripts/mathjax.liquid` |
| Articles | `_articles/`, `_layouts/distill.liquid`, article frontmatter for math options |

