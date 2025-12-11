# Typography & Math Configuration Guide

This document explains how to configure fonts and math rendering across the Spectrum Lab website.

---

## Overview

The site has two main typography control systems:

1. **Site-wide Typography** (`_data/typography.yml`) — Controls fonts for body text, headings, code, and default math settings
2. **Per-article Math Configuration** — Article frontmatter options for math engine and font

---

## Site-wide Typography Configuration

Edit `_data/typography.yml` to change fonts across the entire site.

### Font Families

```yaml
# Body text (paragraphs, general content)
body:
  primary: "Roboto"
  fallback: "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"

# Headings (h1-h6)
headings:
  primary: "Google Sans"
  fallback: "'Roboto', 'Helvetica Neue', sans-serif"

# Code and monospace
code:
  primary: "JetBrains Mono"
  fallback: "'SF Mono', 'Monaco', 'Inconsolata', 'Fira Code', monospace"

# Serif (for articles/blog posts)
serif:
  primary: "Roboto Slab"
  fallback: "Georgia, 'Times New Roman', serif"
```

### Font Weights

```yaml
body:
  weight:
    light: 300
    regular: 400
    medium: 500
    bold: 700
```

### How Fonts Are Applied

The typography configuration generates CSS custom properties:

```css
:root {
  --font-body: Roboto, system-ui, sans-serif;
  --font-heading: Google Sans, 'Roboto', sans-serif;
  --font-code: JetBrains Mono, 'SF Mono', monospace;
  --font-serif: Roboto Slab, Georgia, serif;
}
```

These are then applied to elements via `_includes/typography-styles.liquid`.

---

## Math Rendering Configuration

### Default Settings

In `_data/typography.yml`:

```yaml
math:
  default_engine: "mathjax"  # or "katex"
  
  mathjax:
    version: "3.2.2"
    font: "mathjax-modern"
    output: "chtml"
    tags: "ams"           # Equation numbering style
    inlineMath: true      # Enable $ for inline math
    displayMath: true     # Enable $$ for display math
    processRefs: true     # Process \ref and \eqref
    processEnvironments: true
  
  katex:
    version: "0.16.9"
    font: "katex-main"
    throwOnError: false
    errorColor: "#cc0000"
```

### Per-Article Math Options

Override math settings in any article's frontmatter:

```yaml
---
layout: distill
title: "My Article"

# Math rendering configuration
math_engine: mathjax    # Options: mathjax, katex, false
math_font: mathjax-stix2   # See font options below
enable_math: true       # Set to false to disable math
---
```

### Available Math Fonts

#### MathJax Fonts

| Font Name | Description |
|-----------|-------------|
| `mathjax-modern` | Latin Modern (default, similar to Computer Modern) |
| `mathjax-stix2` | STIX Two fonts (recommended for scientific publishing) |
| `mathjax-termes` | TeX Gyre Termes (Times-like) |
| `mathjax-pagella` | TeX Gyre Pagella (Palatino-like) |
| `mathjax-schola` | TeX Gyre Schola (Century Schoolbook-like) |
| `mathjax-bonum` | TeX Gyre Bonum (Bookman-like) |
| `mathjax-dejavu` | DejaVu fonts |
| `mathjax-fira` | Fira Math |
| `mathjax-gyre` | TeX Gyre fonts |
| `mathjax-asana` | Asana Math |

#### KaTeX Fonts

| Font Name | Description |
|-----------|-------------|
| `katex-main` | Default KaTeX font (Computer Modern-like) |

---

## Example: Different Articles with Different Math Fonts

### Article 1: Using STIX fonts (publication-ready)

```yaml
---
layout: distill
title: "A Mathematical Analysis"
math_engine: mathjax
math_font: mathjax-stix2
---
```

### Article 2: Using Latin Modern (LaTeX classic look)

```yaml
---
layout: distill
title: "Theoretical Foundations"
math_engine: mathjax
math_font: mathjax-modern
---
```

### Article 3: Using KaTeX (faster rendering)

```yaml
---
layout: distill
title: "Quick Calculations"
math_engine: katex
math_font: katex-main
---
```

### Article 4: No math needed

```yaml
---
layout: distill
title: "Non-Technical Overview"
math_engine: false
---
```

---

## Adding New Fonts

### Google Fonts

1. Update the URL in `_config.yml`:

```yaml
third_party_libraries:
  google_fonts:
    url:
      fonts: "https://fonts.googleapis.com/css2?family=YourFont:wght@400;700&display=swap"
```

2. Reference in `_data/typography.yml`:

```yaml
body:
  primary: "YourFont"
```

### Adobe Fonts (Typekit)

1. Update kit ID in `_config.yml`:

```yaml
third_party_libraries:
  adobe_fonts:
    url:
      fonts: "https://use.typekit.net/your-kit-id.css"
```

2. Reference in `_data/typography.yml`.

---

## CSS Custom Properties Reference

Available CSS variables from typography configuration:

```css
/* Font families */
--font-body
--font-heading
--font-code
--font-serif

/* Font weights */
--font-weight-light
--font-weight-regular
--font-weight-medium
--font-weight-bold
--font-weight-heading

/* Font sizes */
--font-size-base
--font-size-small
--font-size-large
--font-size-code
--font-size-h1 through --font-size-h6

/* Line heights */
--line-height-body
--line-height-heading
--line-height-code

/* Letter spacing */
--letter-spacing-body
--letter-spacing-heading
--letter-spacing-code
```

---

## File Locations

| File | Purpose |
|------|---------|
| `_data/typography.yml` | Central typography configuration |
| `_includes/typography-styles.liquid` | Generates CSS custom properties |
| `_includes/scripts/mathjax.liquid` | Math engine loader with per-page config |
| `_includes/core/head.liquid` | Includes typography styles |
| `_sass/_base.scss` | Base SCSS (uses CSS variables) |

---

## Troubleshooting

### Math not rendering

1. Check `enable_math: true` in frontmatter
2. Verify `site.enable_math: true` in `_config.yml`
3. Check browser console for JavaScript errors

### Wrong font showing

1. Verify font is loaded in `_config.yml` (Google Fonts URL)
2. Check font name spelling in `_data/typography.yml`
3. Clear browser cache

### Font FOUT (Flash of Unstyled Text)

The `display: swap` setting in Google Fonts URL helps. For better control, consider:

```yaml
loading:
  strategy: "preload"
  display: "swap"
```
