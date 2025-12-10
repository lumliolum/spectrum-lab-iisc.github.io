# Copilot / AI Agent Instructions — Spectrum Lab website

This repo is a Jekyll-based academic website (al-folio theme) hosted on GitHub Pages. The guidance below focuses on repository-specific structure, developer workflows, and concrete examples an AI coding agent needs to be productive quickly.

- **Big picture:** Jekyll + al-folio theme generate a static site from content in top-level folders (`_pages`, `_posts`, `_people`, `_projects`, `_data`, `_bibliography`). Templates live in `_layouts` and `_includes`. Static assets are under `assets/`. The site is served locally on port `8080` and deployed via GitHub Pages (see `CNAME`).

- **Local development (commands):**
  - Install Ruby gems: ``bundle install``
  - Serve with live reload: ``JEKYLL_ENV=development bundle exec jekyll serve --livereload --port 8080``
  - Build for production: ``JEKYLL_ENV=production bundle exec jekyll build``
  - Docker (dev image provided): ``docker-compose up --build`` or ``docker-compose up`` (volume mounts repo to `/srv/jekyll`, ports `8080` and `35729`).

- **Formatting / editor tooling:**
  - Project includes a Prettier plugin for Liquid in `package.json`. Use: ``npx prettier --plugin=@shopify/prettier-plugin-liquid --write "**/*.{liquid,md,html}"`` to format templates and content.

- **Key files & directories to reference when making changes:**
  - `WEBSITE_GUIDE.md` — canonical, human-maintained developer/content guide (read before making content changes).
  - `_people/person_template.md` — authoritative front-matter fields for adding people (copy & fill).
  - `_bibliography/papers.bib` and `jekyll-scholar` in `Gemfile` — publications are BibTeX-driven; use `person_bibliography.liquid` and `bibliography` templates.
  - `_layouts/default.liquid` and `_includes/*` — site chrome, scripts, and feature flags (look here for where JS/CSS is injected).
  - `Gemfile` — lists Jekyll plugins in use (e.g. `jekyll-jupyter-notebook`, `jekyll-imagemagick`, `jekyll-scholar`) — consult before adding new plugins.

- **Project-specific conventions & patterns:**
  - Data-driven pages: many pages are assembled from YAML in `_data/` (e.g. `people.yml`, `projects.yml`). Modify the YAML or the files under `_people`/`_projects` depending on whether data is centralized or per-item.
  - Person pages: prefer per-person markdown files under `_people/` using the provided template — front-matter keys like `firstname`, `lastname`, `img`, `category`, `show`, and `biography_paragraphs` drive the `person` layout.
  - Publications: maintain `papers.bib` under `_bibliography/`; templates use `jekyll-scholar` conventions and `scholar_userid`/`person_bibliography.liquid` for per-author lists.
  - Notebooks: `jekyll-jupyter-notebook` + `nbconvert` (installed in Dockerfile) — Jupyter notebooks are converted during build; preserve metadata and asset paths.
  - Image handling: `ImageMagick` + `jekyll-imagemagick` are used; optimize images via the documented workflow in `WEBSITE_GUIDE.md`.

- **Build-time environment notes:**
  - Several features rely on native tooling (ImageMagick, nbconvert). The `Dockerfile` installs these to ensure parity with CI/local builds; expect differences if running on a machine without the same system packages.

- **Where to make changes when asked by humans / PRs:**
  - Content updates: edit `_pages`, `_posts`, `_people`, `_projects` or `_data/*.yml` depending on the change.
  - Layout/CSS/JS changes: edit `_layouts/*` and `_includes/*` (preferred) or files under `assets/`.
  - Add new dependencies: update `Gemfile` and run `bundle install` (or update Docker image); document the change in `WEBSITE_GUIDE.md`.

- **Examples an agent can act on immediately:**
  - Add a new person: copy `_people/person_template.md` → `_people/jane-doe.md`, fill front-matter, set `show: true`, commit.
  - Add a publication: append to `_bibliography/papers.bib`, update the author `scholar_userid` if needed, run a local build to confirm rendering.
  - Fix a Liquid bug: check `_layouts/default.liquid` and corresponding `_includes/*` where the snippet is used; use `npx prettier` to format after edits.

- **Caution / gotchas:**
  - Changes that require native binaries (ImageMagick, nbconvert) must be validated in Docker or a matching environment.
  - Many plugins are present; adding or removing plugins can change build output and should be tested locally with `JEKYLL_ENV=production bundle exec jekyll build`.

If anything above is unclear or you want the instructions to emphasize a particular workflow (CI, release, or contributor guidelines), tell me which area to expand and I will iterate.
