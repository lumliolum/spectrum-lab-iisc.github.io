# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

Repository overview
- Static site built with Jekyll, customized from the al-folio theme. Deployed to GitHub Pages from the gh-pages branch via CI on pushes to main.
- Primary technologies: Ruby (Jekyll + plugins), Liquid templates, Markdown content, some Node tooling (Prettier for Liquid). Optional Docker setup for local development.
- Key content areas are modeled as Jekyll collections (people, news, places, alumni) and posts. Publications are rendered via jekyll-scholar from a BibTeX source.

Common commands
- Ruby/Jekyll setup (first run)
  - gem install bundler
  - bundle install

- Local development server (with live reload)
  - JEKYLL_ENV=development bundle exec jekyll serve --livereload --port 8080
  - Site will be available at http://localhost:8080

- Production build
  - JEKYLL_ENV=production bundle exec jekyll build
  - Output is written to _site/ (not committed; CI publishes it)

- Formatting (Prettier + Liquid plugin)
  - Check all files: npx prettier . --check
  - Auto-fix all: npx prettier . --write
  - Single file: npx prettier path/to/file.liquid --check

- Docker (optional)
  - Using docker-compose: docker compose up
    - Exposes: http://localhost:8080 (site) and 35729 (livereload)
    - Uses amirpourmand/al-folio image and mounts the repo. If a local build is attempted and fails due to a missing bin/entry_point.sh, prefer the prebuilt image (compose file already references it).

CI/CD and automation
- Deploy: .github/workflows/jekyll.yml
  - On push to main: sets up Ruby 3.1, installs Jekyll and plugins, builds the site, and publishes _site/ to gh-pages using peaceiris/actions-gh-pages.
- Formatting: .github/workflows/prettier.yml
  - Runs Prettier on pushes/PRs to main/master. On failure, generates and uploads a diff artifact and dispatches a PR notification event.
- Link checking: .github/workflows/broken-links.yml
  - Uses lycheeverse/lychee-action against HTML/Markdown/Liquid assets on push/PR. Certain files and workflows are excluded.
- Accessibility (manual): .github/workflows/axe.yml
  - On workflow_dispatch, builds the site and runs @axe-core/cli with a local http-server and a matching Chrome/chromedriver.
- Lighthouse badges: .github/workflows/lighthouse-badger.yml
  - On page_build (and manual): generates performance badges/reports and commits them back using a repository token.

High-level architecture and content model
- Configuration (_config.yml)
  - Site metadata, URLs, analytics placeholders, Open Graph settings, theme options, includes/excludes, and plugin list.
  - Collections configured for people, news, places, alumni (some output=true, with specific permalinks). Blog pagination and archives are enabled. jekyll-scholar is configured to render publications from _bibliography/papers.bib with APA style and grouping by year.

- Layouts and includes
  - _layouts/default.liquid is the base layout. It handles optional meta refresh redirects (via page.redirect), loads the favicon and head includes, renders the header/footer, and wires in numerous script includes (charts, mermaid, mathjax, etc.).
  - _layouts/person.liquid renders individual person profiles using YAML front matter fields and biography_paragraphs. It encapsulates presentation (including dark theme tweaks) so person markdown files remain data-only.
  - _includes/ contains reusable partials for head, header, footer, social blocks, bib rendering, pagination, scripts, etc. Pages and layouts compose these for consistent structure and behavior.

- Content organization
  - Pages live under _pages/ (e.g., about, blog index, funding, teaching, etc.).
  - Posts are under _posts/ with standard Jekyll naming. Additional assets (e.g., per-post bib files) live under assets/bibliography/ when needed.
  - People profiles live under _people/ and are pure front matter files using layout: person. The person template and documentation live in _people/person_template.md and _people/TEMPLATE_README.md.
  - Publications are sourced from _bibliography/papers.bib and rendered via jekyll-scholar into the publications page.
  - Assets (assets/) include SCSS (compiled to CSS via Jekyll), JS libraries/utilities, images, fonts, favicons, PDFs, and course materials.

Authoring workflows and important notes (from README.md and templates)
- Adding a person
  - Copy _people/person_template.md to _people/<identifier>.md and fill in front matter (layout: person, names, description, img path, category, show flag, and optional fields like email, ORCID, Scholar ID, LinkedIn, GitHub, website). Biography paragraphs can be provided via biography_paragraphs: [ ... ].
  - Place square profile images under assets/img/people/<category>/ and set the img path accordingly.
  - Categories include entries like PhD Students, MSc Students, M.Tech Students, Alumni, Undergraduates, Lab Director (ensure consistency with how the site groups or displays them).

- Adding a publication
  - Edit _bibliography/papers.bib and add entries. jekyll-scholar is configured to render entries on the publications page; optional fields like abstract, doi, pdf, preview, etc., are supported by the templates.

- Organization reminders
  - People images under assets/img/people/[category]/; funding logos under assets/img/funders/; publication previews under assets/img/publication_preview/; lab photos under assets/img/labphotos/.

Local environment expectations
- Ruby tooling via Bundler; Jekyll plugins are declared in Gemfile (jekyll, jekyll-archives, jekyll-scholar, jemoji, etc.). Some workflows also install Jupyter/notebook support; requirements.txt includes nbconvert for notebook processing.
- Node tooling is minimal and focused on Prettier with the @shopify/prettier-plugin-liquid plugin (.prettierrc config present).

Gotchas
- Do not commit _site/; CI builds and deploys it to gh-pages.
- If using Docker and a local build is triggered, note the Dockerfile references bin/entry_point.sh which is not present in this repository; prefer running with the prebuilt image via docker compose up as provided.
