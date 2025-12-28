# People Profile Template System

This directory now uses a clean template system that separates content from presentation:

- **`person_template.md`** - Clean template with only YAML data for easy editing
- **`person.liquid`** (in `_layouts/`) - Handles all HTML structure and styling
- **`css.md`** - Example of the system in use

## How to Create a New Person Profile

1. Copy the `person_template.md` file and rename it to `[person-identifier].md` (e.g., `john-doe.md`)
2. Update the YAML front matter with the person's information
3. The layout will automatically render the profile with proper styling

## YAML Front Matter Variables

## Key Benefits of This System

- **Easy to Edit**: Template files contain only data, no HTML or CSS
- **Consistent Styling**: All profiles use the same layout and appearance
- **Maintainable**: Changes to styling only need to be made in one place (`_layouts/person.liquid`)
- **Clean Separation**: Content editors don't need to worry about HTML/CSS
- **Version Control Friendly**: Simple YAML files are easy to track and merge

### Required Fields
```yaml
layout: person                  # Always "person" (not "page")
title: [Full Name]              # Person's full name
firstname: [First Name]         # First name only
lastname: [Last Name]           # Last name only
description: [Position/Title]   # Job title/position
img: assets/img/people/[category]/[filename.jpg]  # Path to profile photo
category: [Category]            # Lab Director/Faculty/Postdoc/PhD Student/etc.
show: true                      # Whether to show this person on the site
```

### Contact Information (Optional)
```yaml
email: [email@iisc.ac.in]       # Email address (must match _data/emails.yml for bibliography linking)
orcid_id: [ORCID ID]           # ORCID identifier
linkedin_username: [username]   # LinkedIn username
github: [username]              # GitHub username
scholar_userid: [Google Scholar ID]  # Google Scholar user ID
twitter_username: [handle]      # Twitter handle
website: [URL]                  # Personal website URL (displayed on profile)
redirect: [URL]                 # External URL to redirect to when card is clicked (overrides internal profile)
```

### Email Aliases
For the bibliography to correctly link to the person's profile, their email must be mapped to an alias in `_data/emails.yml`.
- If the person has a real email, add it to `_data/emails.yml`.
- If they don't, use a placeholder (e.g., `firstname.lastname@placeholder.com`) in both the profile and `_data/emails.yml`.

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
```yaml
show_awards: true              # Set to false to hide this section
awards:
  - "Award name 1"
  - "Award name 2"
  - "Award name 3"
```

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
website:
orcid_id: 0000-0000-0000-0000
linkedin_username: jane-doe
github: janedoe
email: jane.doe@iisc.ac.in
scholar_userid: abcdefghijk
twitter_username:
website: https://jane-doe.github.io
category: PhD Student
show: true

# Biography content
biography_paragraphs:
  - "Jane Doe is a PhD student in the Electrical Engineering Department at IISc, working under the supervision of Prof. Chandra Sekhar Seelamantula."
  - "Her research interests include machine learning, signal processing, and computer vision."
  - "She received her Bachelor's degree in Electronics and Communication Engineering from XYZ University in 2020."

# Academic and Editorial Roles (optional section)
show_academic_roles: false
academic_roles: []

# Awards (optional section)
show_awards: true
awards:
  - "Best Paper Award, Conference XYZ 2023"
  - "Graduate Student Fellowship, IISc 2021-2024"

# Visiting Positions (optional section)
show_visiting_positions: false
visiting_positions: []
---
```

## Notes

- **Layout**: Always use `layout: person` (not `layout: page`)
- **Optional Sections**: Set `show_academic_roles: false`, `show_awards: false`, or `show_visiting_positions: false` to hide sections that don't apply
- **Empty Sections**: If a section is hidden, you can leave the corresponding array empty or omit it entirely
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
│   ├── mtech-students/
│   ├── mtech-research/
│   └── project-associates/
└── alumni/                # Graduated members
    ├── phd-graduates/
    ├── mtech-graduates/
    └── mtech-research-graduates/

_layouts/
└── person.liquid          # Layout file that renders all profiles
```
