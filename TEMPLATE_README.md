# People Profile Template System

This directory now uses a clean template system that separates content from presentation:

- **`person_template.md`** - Clean template with only YAML data for easy editing
- **`person.liquid`** (in `_layouts/`) - Handles all HTML structure and styling
- **`css.md`** - Example of the system in use

## How to Create a New Person Profile

1. Copy the `person_template.md` file and rename it to `[person-identifier].md` (e.g., `john-doe.md`)
2. Update the YAML front matter with the person's information
3. Run the build - the `ensure_person_fields.py` script will auto-fill missing email/alias
4. The layout will automatically render the profile with proper styling

## YAML Front Matter Variables

## Key Benefits of This System

- **Easy to Edit**: Template files contain only data, no HTML or CSS
- **Consistent Styling**: All profiles use the same layout and appearance
- **Maintainable**: Changes to styling only need to be made in one place (`_layouts/person.liquid`)
- **Clean Separation**: Content editors don't need to worry about HTML/CSS
- **Version Control Friendly**: Simple YAML files are easy to track and merge
- **Auto-fill**: Missing email and alias fields are auto-generated on build

### Required Fields
```yaml
layout: person                  # Always "person" (not "page")
title: [Full Name]              # Person's full name
firstname: [First Name]         # First name only
lastname: [Last Name]           # Last name only
description: [Position/Title]   # Job title/position
img: assets/img/people/[category]/[filename.jpg]  # Path to profile photo
category: [Category]            # Lab Director/Faculty/Postdoc/PhD Student/etc.
year: [YYYY]                    # Year of graduation (for alumni) or cohort year (for students)
show: true                      # Whether to show this person on the site
```

### Contact Information (Optional)
```yaml
email: [email@iisc.ac.in]       # Email address
alias: [unique_alias]           # Unique alias for bibliography and recognition linking
orcid_id: [ORCID ID]           # ORCID identifier
linkedin_username: [username]   # LinkedIn username
github: [username]              # GitHub username
scholar_userid: [Google Scholar ID]  # Google Scholar user ID
twitter_username: [handle]      # Twitter handle
website: [URL]                  # Personal website URL (displayed on profile)
redirect: [URL]                 # External URL to redirect to when card is clicked (overrides internal profile)
```

### Alias Field
The `alias` field is used to link profiles to:
- **Publications** in `_bibliography/papers.bib` (via the `emails` field)
- **Awards** in `_data/recognition.yml` (via the `aliases` field)

If not provided, the build script will auto-generate an alias from the filename.

### Biography Content
```yaml
biography_paragraphs:
  - "First paragraph of biography..."
  - "Second paragraph of biography..."
  - "Third paragraph of biography..."
```

### Academic and Editorial Roles (Optional Section)
```yaml
show_academic_roles: true       # Set to false to hide this section
academic_roles:
  - "Role description 1"
  - "Role description 2"
  - "Role description 3"
```

### Awards (Optional Section)
Awards are now automatically fetched from `_data/recognition.yml` based on the person's alias.
No need to add them manually to individual profiles.

### Visiting Positions (Optional Section)
```yaml
show_visiting_positions: true   # Set to false to hide this section
visiting_positions:
  - institution: "Institution Name"
    dates: "Date Range"
    hosts: "Host Name(s)"
  - institution: "Another Institution"
    dates: "Date Range"
    hosts: "Host Name(s)"
```

## Example Template

```yaml
---
layout: person
title: Jane Doe
firstname: Jane
lastname: Doe
description: PhD Student
img: assets/img/people/phd_students/jane-doe.jpg
email: jane.doe@iisc.ac.in
alias: jane_doe
orcid_id: 0000-0000-0000-0000
linkedin_username: jane-doe
github: janedoe
scholar_userid: abcdefghijk
twitter_username:
website: https://jane-doe.github.io
category: PhD Student
year: 2024
show: true

# Biography content
biography_paragraphs:
  - "Jane Doe is a PhD student in the Electrical Engineering Department at IISc, working under the supervision of Prof. Chandra Sekhar Seelamantula."
  - "Her research interests include machine learning, signal processing, and computer vision."
  - "She received her Bachelor's degree in Electronics and Communication Engineering from XYZ University in 2020."

# Academic and Editorial Roles (optional section)
show_academic_roles: false
academic_roles: []

# Visiting Positions (optional section)
show_visiting_positions: false
visiting_positions: []
---
```

## Notes

- **Layout**: Always use `layout: person` (not `layout: page`)
- **Alias**: Used for linking to publications and awards (auto-generated if missing)
- **Awards**: Automatically displayed from `_data/recognition.yml` if alias matches
- **Optional Sections**: Set `show_academic_roles: false` or `show_visiting_positions: false` to hide sections
- **Host Detection**: The template automatically handles singular vs. plural for hosts ("Host:" vs "Hosts:")
- **Styling**: All HTML and CSS is handled by the `person.liquid` layout file
- **Dark Theme**: Dark theme support is built into the layout
- **Fallback**: If you don't use `biography_paragraphs`, any content in the markdown body will be displayed as biography

## File Structure

```
_people/
├── person_template.md     # Template for new profiles
├── TEMPLATE_README.md     # This documentation
├── current/               # Current lab members
│   ├── lab-director/
│   ├── administrator/
│   ├── phd-students/
│   ├── mtech-students/    # Grouped by cohort year (e.g., 2026/)
│   ├── mtech-research/
│   └── project-associates/
└── alumni/                # Graduated members (Grouped by year)
    ├── phd-graduates/     # e.g., 2024/
    ├── mtech-graduates/   # e.g., 2023/
    └── mtech-research-graduates/

_layouts/
└── person.liquid          # Layout file that renders all profiles

scripts/
└── ensure_person_fields.py  # Auto-fills missing email/alias on build
```
