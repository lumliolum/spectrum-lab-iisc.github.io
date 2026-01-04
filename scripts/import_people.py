#!/usr/bin/env python3
"""
Import people from people.xlsx and create Jekyll person markdown files.

Usage:
  conda activate localEnv
  python scripts/import_people.py

The script expects `people.xlsx` at the repo root and photos in `people_photos/`.
It writes markdown files to `_people/current/<category>/` and copies photos to
`assets/img/people/<category>/`.
"""
import os
import re
import shutil
from pathlib import Path

try:
    import pandas as pd
except Exception as e:
    print("Missing pandas dependency. Please install in localEnv: conda install -n localEnv pandas openpyxl")
    raise


ROOT = Path(__file__).resolve().parents[1]
XL_PATH = ROOT / "people.xlsx"
PHOTOS_DIR = ROOT / "people_photos"
PEOPLE_DIR_CURRENT = ROOT / "_people" / "current"
PEOPLE_DIR_ALUMNI = ROOT / "_people" / "alumni"
ASSETS_IMG_ROOT = ROOT / "assets" / "img" / "people"

# Map "Graduated as:" values to alumni folder names (for _people)
GRADUATED_TO_FOLDER = {
    'phd': 'phd-graduates',
    'm.tech research': 'mtech-research-graduates',
    'm.tech (previously m.e.)': 'mtech-graduates',
    'project associate/ research associate': 'research-associates',
    'intern': 'interns',
}

# Map to image folder names (under assets/img/people/alumni/)
GRADUATED_TO_IMG_FOLDER = {
    'phd': 'phd',
    'm.tech research': 'mtech-research',
    'm.tech (previously m.e.)': 'mtech',
    'project associate/ research associate': 'research-associates',
    'intern': 'interns',
}

# Category display names
GRADUATED_TO_CATEGORY = {
    'phd': 'PhD Graduates',
    'm.tech research': 'M.Tech Research Graduates',
    'm.tech (previously m.e.)': 'M.Tech Graduates',
    'project associate/ research associate': 'Research Associates',
    'intern': 'Interns',
}


def slugify(s: str) -> str:
    s = s or ""
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s)
    s = s.strip("-")
    return s or "unknown"


def choose_col(df, options):
    for o in options:
        if o in df.columns:
            return o
    return None


def read_sheet(path):
    df = pd.read_excel(path, engine="openpyxl")
    # normalize columns
    df.columns = [c.strip() if isinstance(c, str) else c for c in df.columns]
    return df


def format_front_matter(d):
    lines = ["---"]
    # required base fields
    lines.append(f"layout: person")
    title = f"{d.get('firstname','').strip()} {d.get('lastname','').strip()}".strip()
    lines.append(f"title: {title}")
    if d.get('firstname'):
        lines.append(f"firstname: {d.get('firstname').strip()}")
    if d.get('lastname'):
        lines.append(f"lastname: {d.get('lastname').strip()}")
    if d.get('description'):
        lines.append(f"description: {d.get('description').strip()}")
    if d.get('img'):
        lines.append(f"img: {d.get('img')}")
    for field in ("website","orcid_id","linkedin_username","github","email","scholar_userid","twitter_username"):
        if d.get(field):
            lines.append(f"{field}: {d.get(field)}")
    if d.get('category'):
        lines.append(f"category: {d.get('category')}")
    lines.append("show: true")
    if d.get('year'):
        lines.append(f"year: {d.get('year')}")
    lines.append("")

    # biography paragraphs
    bio_pars = d.get('biography_paragraphs', [])
    if bio_pars:
        lines.append("biography_paragraphs:")
        for p in bio_pars:
            safe = p.replace('"', '\\"')
            lines.append(f"  - \"{safe}\"")

    # keep optional sections as false by default
    lines.append("")
    lines.append("show_academic_roles: false")
    lines.append("academic_roles: []")
    lines.append("")
    lines.append("show_awards: false")
    lines.append("awards: []")
    lines.append("")
    lines.append("badges: []")
    lines.append("")
    lines.append("show_visiting_positions: false")
    lines.append("visiting_positions: []")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def main():
    if not XL_PATH.exists():
        print(f"Excel file not found at {XL_PATH}")
        return
    df = read_sheet(XL_PATH)

    # common column mappings
    col_map = {
        'firstname': ['firstname','first_name','first name','first'],
        'lastname': ['lastname','last_name','last name','last'],
        'description': ['description','title','position','role'],
        'email': ['email','e-mail'],
        'category': ['category','group','role_category'],
        'img': ['img','image','photo','photo_filename','photo filename','filename'],
        'website': ['website','url'],
        'orcid_id': ['orcid','orcid_id'],
        'linkedin_username': ['linkedin_username','linkedin','linkedin_url'],
        'github': ['github','github_username','github_url'],
        'scholar_userid': ['scholar_userid','google_scholar','scholar'],
        'twitter_username': ['twitter','twitter_username','twitter_handle'],
        'biography': ['biography','bio','about']
    }

    # detect columns (exact matches first, then substring matches for noisy headers)
    detected = {}
    lc = [c.lower() if isinstance(c,str) else c for c in df.columns]
    for key, opts in col_map.items():
        for o in opts:
            if o in lc:
                for orig in df.columns:
                    if isinstance(orig, str) and orig.lower() == o:
                        detected[key] = orig
                        break
                if key in detected:
                    break

    # handle common actual headers in the provided sheet
    for orig in df.columns:
        if not isinstance(orig, str):
            continue
        low = orig.lower()
        if 'full name' in low or low.strip() == 'name' or 'full name' == low:
            detected.setdefault('fullname', orig)
        if 'photograph' in low or 'photograph' in low:
            detected.setdefault('img', orig)
        if 'brief biography' in low or 'biography' in low or 'about' in low:
            detected.setdefault('biography', orig)
        if 'professional role' in low or 'role/affiliation' in low or 'current professional' in low:
            detected.setdefault('description', orig)
        if 'website' in low and 'url' in low:
            detected.setdefault('website', orig)
        if 'google scholar' in low or 'scholar' in low:
            detected.setdefault('scholar_userid', orig)
        if 'email' in low and 'your current' in low:
            detected.setdefault('email', orig)

    # Detect "Graduated as:" column
    graduated_col = None
    year_col = None
    for orig in df.columns:
        if isinstance(orig, str):
            if 'graduated as' in orig.lower():
                graduated_col = orig
            if 'year of graduation' in orig.lower():
                year_col = orig

    created = []
    skipped = []
    for idx, row in df.iterrows():
        if detected.get('fullname'):
            full = str(row.get(detected.get('fullname'), '')).strip()
            parts = full.split()
            first = parts[0] if parts else ''
            last = ' '.join(parts[1:]) if len(parts) > 1 else ''
        else:
            first = str(row.get(detected.get('firstname',''), '')).strip()
            last = str(row.get(detected.get('lastname',''), '')).strip()
        if not first and not last:
            skipped.append((idx, 'no name'))
            continue

        # Use "Graduated as:" column for category -> alumni folder
        graduated_as = ''
        if graduated_col:
            graduated_as = str(row.get(graduated_col, '')).strip().lower()
        
        folder_name = GRADUATED_TO_FOLDER.get(graduated_as, 'phd-graduates')
        img_folder_name = GRADUATED_TO_IMG_FOLDER.get(graduated_as, 'phd')
        category = GRADUATED_TO_CATEGORY.get(graduated_as, 'PhD Graduates')

        # Get graduation year
        year = ''
        if year_col:
            year_val = row.get(year_col, '')
            if pd.notna(year_val):
                year_str = str(int(year_val)) if isinstance(year_val, float) else str(year_val).strip()
                # Extract just the 4-digit year (handle messy data like "2017, Spectrum Lab, PhD")
                import re as re_inner
                match = re_inner.search(r'\b(20\d{2})\b', year_str)
                year = match.group(1) if match else year_str
        if not year or not year.isdigit():
            year = 'unknown'

        # All people from this spreadsheet are alumni - year-wise folders
        person_dir = PEOPLE_DIR_ALUMNI / folder_name / year
        person_dir.mkdir(parents=True, exist_ok=True)
        img_dir = ASSETS_IMG_ROOT / "alumni" / img_folder_name / year
        img_dir.mkdir(parents=True, exist_ok=True)

        # photo handling
        photo = row.get(detected.get('img',''), '') if detected.get('img') else ''
        photo = str(photo).strip()
        img_rel_path = ''
        if photo:
            src_photo = PHOTOS_DIR / photo
            if not src_photo.exists():
                # try with common extensions
                candidates = [PHOTOS_DIR / (photo + ext) for ext in ['.jpg','.jpeg','.png','.webp']]
                found = None
                for c in candidates:
                    if c.exists():
                        found = c
                        break
                if found:
                    src_photo = found
                else:
                    print(f"Warning: photo {photo} not found for {first} {last}")
                    src_photo = None
            if src_photo:
                dest = img_dir / src_photo.name
                try:
                    shutil.copy2(src_photo, dest)
                    img_rel_path = f"assets/img/people/alumni/{img_folder_name}/{year}/{src_photo.name}"
                except Exception as e:
                    print(f"Failed to copy photo for {first} {last}: {e}")

        # biography parsing
        bio_raw = row.get(detected.get('biography',''), '') if detected.get('biography') else ''
        bio_pars = []
        if isinstance(bio_raw, str) and bio_raw.strip():
            # split on double newlines or single newlines
            parts = [p.strip() for p in re.split(r"\n\n+", bio_raw) if p.strip()]
            if not parts:
                parts = [p.strip() for p in bio_raw.split('\n') if p.strip()]
            bio_pars = parts

        record = {
            'firstname': first,
            'lastname': last,
            'description': str(row.get(detected.get('description',''), '')).strip(),
            'img': img_rel_path,
            'website': str(row.get(detected.get('website',''), '')).strip(),
            'orcid_id': str(row.get(detected.get('orcid_id',''), '')).strip(),
            'linkedin_username': str(row.get(detected.get('linkedin_username',''), '')).strip(),
            'github': str(row.get(detected.get('github',''), '')).strip(),
            'email': str(row.get(detected.get('email',''), '')).strip(),
            'scholar_userid': str(row.get(detected.get('scholar_userid',''), '')).strip(),
            'twitter_username': str(row.get(detected.get('twitter_username',''), '')).strip(),
            'category': category,
            'year': year,
            'biography_paragraphs': bio_pars,
        }

        # filename
        fname = slugify(f"{first} {last}") or f"person-{idx}"
        file_path = person_dir / f"{fname}.md"
        
        # Check if person already exists anywhere in _people/alumni
        existing = list(PEOPLE_DIR_ALUMNI.rglob(f"*{fname}*.md")) + list(PEOPLE_DIR_ALUMNI.rglob(f"*{slugify(first)}*{slugify(last)}*.md"))
        # Also check with underscore naming convention
        fname_underscore = f"{slugify(first)}_{slugify(last)}".replace('-', '_')
        existing += list(PEOPLE_DIR_ALUMNI.rglob(f"*{fname_underscore}*.md"))
        if existing:
            skipped.append((idx, f'{first} {last} - already exists: {existing[0].name}'))
            continue
        
        content = format_front_matter(record)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        created.append(str(file_path))

    print(f"Created {len(created)} person files")
    if created:
        for p in created:
            print(f" - {p}")
    if skipped:
        print(f"Skipped {len(skipped)} rows:")
        for s in skipped:
            print(f"  - Row {s[0]}: {s[1]}")


if __name__ == '__main__':
    main()
