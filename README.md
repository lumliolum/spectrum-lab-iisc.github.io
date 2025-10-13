# Spectrum Lab Website Documentation

## People Navigation

The People section uses a dropdown navigation system to organize team members by categories. This provides better navigation and cleaner organization compared to displaying everyone on a single long page.

### Navigation Structure

The People dropdown includes:
- **All People** - Shows everyone (main people page)
- **PhD Students** - Current PhD students
- **Project Associates** - Current project associates
- **M.Tech Students** - Current M.Tech students
- **PhD Graduates** - PhD graduates from the lab
- **MTech (Res.) Graduates** - MTech (Research) graduates
- **Administrator** - Administrative staff

### How It Works

The dropdown navigation is configured in `_pages/people.md` with the `dropdown: true` setting and a `children:` list that defines each category page. Individual category pages are located in `_pages/people/` and use the `people_category` layout to display people filtered by category.

## Adding People, Categories, and Publications

## Adding a Person

To add a person to the website:

1. **Create a Markdown file** in the `_people` directory. Use the format: `firstname_lastname.md`.
2. **Use the following template** in your Markdown file:

    ```yaml
    ---
    layout: about
    firstname: Firstname
    lastname: Lastname
    description: Your description here
    img: path/to/image.jpg # Ensure this path is correct
    redirect: https://link-to-profile
    linkedin_username: linkedin_handle
    github_username: github_handle
    email: your-email@example.com
    category: Your category here
    show: true # or false to hide
    ---
    ```

3. **Upload an Image**: Place the image in the appropriate category folder within `assets/img/people/`:
   - `assets/img/people/phd/` for PhD Students
   - `assets/img/people/mtech/` for M.Tech Students
   - `assets/img/people/alumni/` for Alumni
   - `assets/img/people/project-associates/` for Project Associates
**Necessarily make the image square**

4. **Category**: You can categorize people as "PhD Students", "Project Associates", "M.Tech Students", "PhD Graduates", "MTech (Res.) Graduates", or "Administrator". Add accordingly under `category`. The category must match exactly with the categories defined in the People dropdown.

5. **Image Path**: Update the `img:` field to reflect the correct folder structure, e.g., `assets/img/people/phd/yourname.jpg`

## Managing People Categories

### Adding a New Category

To add a new people category to the dropdown:

1. **Create a category page**: Create a new file in `_pages/people/` (e.g., `new-category.md`) with:
   ```yaml
   ---
   layout: people_category
   title: New Category
   permalink: /people/new-category/
   category: New Category
   description: Description for this category
   nav: false
   ---
   ```

2. **Update the main People page**: Edit `_pages/people.md` to add the new category to the `children:` list and `display_categories:` list.

3. **Update image folders**: Create corresponding folders in `assets/img/people/` if needed.

### Removing a Category

1. Delete the category page from `_pages/people/`
2. Remove the category from the `children:` and `display_categories:` lists in `_pages/people.md`
3. Move or reassign people from that category to other categories

## Categories

Categories can be defined for organizing both people and collections:

- **People Categories**: Defined directly in each `_people/firstname_lastname.md` file under the `category` tag.
- **Project/Collection Categories**: Adjust these in the `_config.yml` file under collections or directly within each project/article markdown files.

## Adding a Publication

To add a publication:

1. **Edit the BibTeX file** located at `_bibliography/papers.bib`.
2. **Add a BibTeX entry** using the following template:

    ```bibtex
    @article{author2023title,
      author       = {Author, A. and Another, B.},
      title        = {Title of the Work},
      journal      = {Journal Name},
      year         = {2023},
      volume       = {10},
      number       = {1},
      pages        = {1--10},
      url          = {https://link.to/publication},
      bibtex_show  = {true}
    }
    ```

3. **Additional Info**: Optional fields include `abstract`, `doi`, `pdf`, etc., which can be linked in the assets directory.

## Technical Implementation Details

### People Dropdown System

The People dropdown navigation system consists of:

1. **Main People Page** (`_pages/people.md`):
   - Contains `dropdown: true` to enable dropdown functionality
   - Defines `children:` list with links to category pages
   - Maintains `display_categories:` for backward compatibility
   - Shows all people when accessed directly at `/people/`

2. **Category Pages** (`_pages/people/*.md`):
   - Use `layout: people_category` for consistent display
   - Filter people by the specified `category` field
   - Individual pages for each category (e.g., `/people/phd-students/`)

3. **People Category Layout** (`_layouts/people_category.liquid`):
   - Reusable layout that filters and displays people by category
   - Maintains the same styling and functionality as the original people page
   - Handles empty states when no people exist in a category

4. **Navigation Integration**:
   - Header automatically detects `dropdown: true` in page front matter
   - Renders dropdown menu with children links
   - Supports dividers and active state highlighting

### File Structure
```
_pages/
├── people.md                    # Main people page with dropdown config
└── people/
    ├── phd-students.md          # PhD Students category page
    ├── project-associates.md     # Project Associates category page
    ├── mtech-students.md        # M.Tech Students category page
    ├── phd-graduates.md         # PhD Graduates category page
    ├── mtech-res-graduates.md   # MTech (Res.) Graduates category page
    └── administrator.md         # Administrator category page

_layouts/
└── people_category.liquid       # Layout for category pages
```

## Organization Structure

The assets are organized in the following folder structure:

- **People Images**: `assets/img/people/[category]/` - Images organized by role (phd, msc, mtech, alumni, undergraduates, lab_director)
- **Funding Logos**: `assets/img/funders/` - All funding organization logos and sponsor images
- **Publication Previews**: `assets/img/publication_preview/` - Preview images for publications
- **Lab Photos**: `assets/img/labphotos/` - Laboratory and facility photos
- **Project Images**: Various project-specific folders for related images


