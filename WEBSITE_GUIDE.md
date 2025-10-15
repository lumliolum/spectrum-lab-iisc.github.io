# Spectrum Lab Website Management Guide

## 🏠 Overview

This is the comprehensive guide for managing the Spectrum Lab website built with Jekyll and deployed on GitHub Pages. The website uses the al-folio theme with custom modifications for lab-specific needs.

**Website URL:** https://spectrum-lab-iisc.github.io  
**Repository:** https://github.com/spectrum-lab-iisc/spectrum-lab-iisc.github.io

---

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Adding People](#adding-people)
- [Managing Publications](#managing-publications)
- [Adding News](#adding-news)
- [Managing Teaching Content](#managing-teaching-content)
- [Managing Research/Projects](#managing-researchprojects)
- [Image Management](#image-management)
- [Development Setup](#development-setup)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)

---

## ⚡ Quick Start

### Local Development
```bash
# Install dependencies (first time only)
gem install bundler
bundle install

# Start local development server
JEKYLL_ENV=development bundle exec jekyll serve --livereload --port 8080

# Access site at: http://localhost:8080
```

### Production Build
```bash
JEKYLL_ENV=production bundle exec jekyll build
```

---

## 👥 Adding People

### Directory Structure
People are organized in `_people/` with subdirectories by category:
```
_people/
├── lab-director/             # Lab director (Prof. CSS)
├── phd-students/             # Current PhD students  
├── phd-graduates/            # PhD graduates (with redirects)
├── mtech-students/           # Current M.Tech students
├── mtech-research/           # Current M.Tech Research students
├── mtech-research-graduates/ # M.Tech Research graduates
├── project-associates/       # Project associates
├── administrator/            # Administrative staff
├── person_template.md        # Template for new profiles
└── TEMPLATE_README.md        # Template documentation
```

### Adding a New Person

1. **Copy the template:**
   ```bash
   cp _people/person_template.md _people/[category]/[firstname-lastname].md
   ```

2. **Update the YAML front matter:**
   ```yaml
   ---
   layout: person
   title: John Doe
   firstname: John
   lastname: Doe
   description: PhD Student
   img: assets/img/people/phd/john-doe.jpg
   email: john.doe@iisc.ac.in
   category: PhD Students
   show: true
   
   # Optional fields
   website: https://john-doe.github.io
   linkedin_username: john-doe
   github_username: johndoe
   scholar_userid: ABC123DEF456
   orcid_id: 0000-0000-0000-0000
   
   # Biography
   biography_paragraphs:
     - "John Doe is a PhD student..."
     - "His research interests include..."
   ---
   ```

3. **Add profile image:**
   - Place square image in `assets/img/people/[category]/`
   - Supported formats: `.jpg`, `.jpeg`, `.png`
   - Recommended size: 400x400 pixels or larger (square aspect ratio)

### Person Categories
- **Lab Director**: `category: Lab Director`
- **PhD Students**: `category: PhD Students`  
- **PhD Graduates**: `category: PhD Graduates` (use `redirect:` instead of `website:`)
- **M.Tech Students**: `category: M.Tech Students`
- **M.Tech Research Students**: `category: M.Tech Research Students`
- **M.Tech Research Graduates**: `category: M.Tech Research Graduates`
- **Project Associates**: `category: Project Associates`
- **Administrator**: `category: Administrator`

### Special Notes for PhD Graduates
For PhD graduates, use `redirect:` field instead of `website:` to automatically redirect their individual pages to their current websites:
```yaml
redirect: https://their-current-website.com
```

---

## 📚 Managing Publications

Publications are managed through a BibTeX file and jekyll-scholar plugin.

### Adding Publications

1. **Edit the BibTeX file:**
   ```bash
   vim _bibliography/papers.bib
   ```

2. **Add BibTeX entries:**
   ```bibtex
   @article{doe2024method,
     title={Novel Method for Signal Processing},
     author={Doe, John and Seelamantula, Chandra Sekhar},
     journal={IEEE Transactions on Signal Processing},
     volume={72},
     number={1}, 
     pages={1--15},
     year={2024},
     publisher={IEEE},
     doi={10.1109/TSP.2024.1234567},
     url={https://ieeexplore.ieee.org/document/1234567},
     pdf={doe2024method.pdf},
     bibtex_show={true},
     preview={doe2024method.jpg}
   }
   ```

3. **Optional fields:**
   - `abstract`: Paper abstract
   - `pdf`: PDF filename (place in `assets/pdf/`)
   - `preview`: Preview image (place in `assets/img/publication_preview/`)
   - `code`: Link to code repository
   - `slides`: Link to presentation slides
   - `website`: Project website
   - `video`: Video presentation link

### Author-Specific Publications
Publications are automatically filtered by author email in individual person profiles. The system uses the `emails` field in BibTeX entries to match publications to people.

---

## 📰 Adding News

News items are stored in `_news/` directory.

### Adding News Item

1. **Create news file:**
   ```bash
   vim _news/YYYY-MM-DD-short-title.md
   ```

2. **Add front matter:**
   ```yaml
   ---
   layout: post
   title: Paper Accepted at ICASSP 2024
   date: 2024-01-15
   inline: false  # false for full news post, true for inline
   related_posts: false
   ---
   
   Our paper "Novel Signal Processing Method" has been accepted at ICASSP 2024.
   
   More details about the work can be found [here](link-to-paper).
   ```

### Inline vs Full News Posts
- **Inline (`inline: true`)**: Short news items displayed directly on news page
- **Full (`inline: false`)**: Full news posts with individual pages

---

## 🎓 Managing Teaching Content  

Teaching pages are in `_pages/teaching/`.

### Adding New Course

1. **Create course page:**
   ```bash
   vim _pages/teaching/course-name.md
   ```

2. **Add course content:**
   ```yaml
   ---
   layout: page
   title: Course Name
   description: Brief course description
   img: assets/img/teaching/course-banner.jpg
   importance: 1
   category: current  # or "past"
   ---
   
   ## Course Overview
   
   Course description and details...
   
   ## Syllabus
   
   - Topic 1
   - Topic 2
   
   ## Resources
   
   - [Lecture Notes](link)
   - [Assignments](link)
   ```

### Course Materials
Place course materials in `assets/pdf/teaching/` or link to external resources.

---

## 🔬 Managing Research/Projects

Research projects can be managed through pages or collections.

### Adding Research Area Page

1. **Create research page:**
   ```bash
   vim _pages/research/research-area.md
   ```

2. **Add research content:**
   ```yaml
   ---
   layout: page  
   title: Research Area Name
   description: Brief description of research area
   img: assets/img/research/area-banner.jpg
   importance: 1
   ---
   
   ## Overview
   
   Research area description...
   
   ## Current Projects
   
   - Project 1
   - Project 2
   
   ## Publications
   
   Key publications in this area...
   ```

---

## 🖼️ Image Management

### Directory Structure
```
assets/img/
├── people/
│   ├── phd/                    # PhD student photos
│   ├── mtech/                  # M.Tech student photos  
│   ├── mtech-research/         # M.Tech Research student photos
│   ├── lab_director/           # Lab director photo
│   ├── phd-graduates/          # PhD graduate photos
│   ├── mtech-research-graduates/ # M.Tech Research graduate photos
│   ├── project-associates/     # Project associate photos
│   └── administrator/          # Administrator photos
├── publication_preview/  # Publication preview images
├── funders/             # Funding agency logos
├── news/               # News-related images
├── teaching/           # Teaching-related images
├── research/           # Research-related images
└── album/              # Gallery images
```

### Image Guidelines
- **Profile Photos**: Square aspect ratio (400x400px minimum)
- **Publication Previews**: 16:9 or 4:3 aspect ratio
- **News Images**: Variable sizes, optimize for web
- **Formats**: `.jpg`, `.jpeg`, `.png` supported
- **Optimization**: Images are automatically optimized by jekyll-imagemagick

### Responsive Images
The site automatically generates responsive images in multiple sizes (480px, 800px, 1400px) and WebP format for better performance.

---

## 💻 Development Setup

### Prerequisites
- Ruby (3.2 or higher)
- Bundler gem
- ImageMagick (for image processing)
- Node.js (for Prettier formatting)

### First Time Setup
```bash
# Install Ruby dependencies
gem install bundler
bundle install

# Install Node.js dependencies (for formatting)
npm install

# Install ImageMagick (macOS)
brew install imagemagick

# Install ImageMagick (Ubuntu)
sudo apt-get install imagemagick libmagickwand-dev
```

### Development Commands
```bash
# Start development server
JEKYLL_ENV=development bundle exec jekyll serve --livereload --port 8080

# Build for production
JEKYLL_ENV=production bundle exec jekyll build

# Format code
npx prettier . --write

# Check formatting
npx prettier . --check
```

### Docker Development (Optional)
```bash
# Start with docker-compose
docker compose up

# Access at: http://localhost:8080
# LiveReload: port 35729
```

---

## 🚀 Deployment

### Automatic Deployment
The site automatically deploys via GitHub Actions when you push to the `main` branch.

### GitHub Actions Workflow
- **Trigger**: Push to `main` branch
- **Build**: Jekyll build with Ruby 3.2
- **Deploy**: To `gh-pages` branch via GitHub Pages
- **Features**: ImageMagick processing, responsive images, minification

### Manual Deployment
If needed, you can trigger manual deployment:
1. Go to GitHub repository
2. Click "Actions" tab  
3. Select "Jekyll Deploy" workflow
4. Click "Run workflow"

---

## 🔧 Troubleshooting

### Common Issues

#### ImageMagick Errors
```bash
# Verify ImageMagick installation
convert -version

# Check for WebP support
convert -list format | grep -i webp

# Fix permissions (if needed)
sudo chmod 644 /etc/ImageMagick-6/policy.xml
```

#### Ruby Version Issues
```bash
# Check Ruby version
ruby --version

# Install correct Ruby version (using rbenv)
rbenv install 3.2.0
rbenv local 3.2.0
```

#### Bundle Install Failures
```bash
# Clear bundle cache
bundle clean --force
bundle install

# Update Gemfile.lock
bundle update
```

#### Jupyter Notebook Issues
```bash
# Install Jupyter
pip3 install jupyter nbconvert

# Verify installation
jupyter --version
```

### Build Failures
1. Check GitHub Actions logs
2. Verify all images exist and paths are correct
3. Check YAML front matter syntax
4. Ensure all required gems are in Gemfile

### Performance Issues
- Optimize images before uploading
- Use appropriate image formats (WebP when possible)
- Minimize large files in repository

---

## 📝 Content Guidelines

### Writing Style
- Use clear, concise language
- Follow academic writing standards
- Include relevant links and references

### Image Guidelines  
- Use high-quality, professional images
- Ensure proper attribution for external images
- Optimize file sizes for web performance

### SEO Best Practices
- Use descriptive page titles
- Include meta descriptions
- Use proper heading hierarchy (H1, H2, H3)
- Add alt text to images

---

## 📞 Support

For technical issues or questions:
1. Check this documentation
2. Review GitHub Issues in the repository
3. Contact the website maintainer
4. Refer to Jekyll and al-folio documentation

### Useful Resources
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [al-folio Theme](https://github.com/alshedivat/al-folio)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Liquid Template Language](https://shopify.github.io/liquid/)

---

*Last Updated: October 2024*