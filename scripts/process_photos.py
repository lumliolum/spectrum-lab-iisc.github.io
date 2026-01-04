#!/usr/bin/env python3
"""
Match downloaded photos to new alumni profiles, make them square, and update markdown files.
"""
from __future__ import annotations
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHOTOS_DIR = ROOT / 'people_photos'
PEOPLE_DIR = ROOT / '_people' / 'alumni'
ASSETS_IMG = ROOT / 'assets' / 'img' / 'people' / 'alumni'

def slugify(s):
    s = s or ""
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")

def extract_name_from_photo(filename):
    # Photos have format like "something - Name.ext"
    match = re.search(r' - ([^.]+)\.(jpe?g|png|JPG|JPEG|PNG)$', filename, re.I)
    if match:
        return match.group(1).strip()
    return None

def make_square_crop(src, dest):
    """Use ImageMagick to center-crop to square 400x400"""
    dest.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        'magick', str(src),
        '-gravity', 'center',
        '-thumbnail', '400x400^',
        '-extent', '400x400',
        '-quality', '85',
        str(dest)
    ]
    subprocess.run(cmd, check=True)

def update_md_img(md_path, img_rel_path):
    """Update the img: field in markdown front matter"""
    text = md_path.read_text(encoding='utf-8')
    if re.search(r'^img:\s*$', text, re.M):
        # Empty img field, add the path
        text = re.sub(r'^img:\s*$', f'img: {img_rel_path}', text, flags=re.M)
    elif not re.search(r'^img:', text, re.M):
        # No img field, add after description
        text = re.sub(r'(^description:.*$)', f'\\1\nimg: {img_rel_path}', text, flags=re.M)
    else:
        # Has img field, replace
        text = re.sub(r'^img:.*$', f'img: {img_rel_path}', text, flags=re.M)
    md_path.write_text(text, encoding='utf-8')

def names_match(photo_name, file_slug):
    """Fuzzy match photo name to file slug"""
    pn = slugify(photo_name)
    fs = file_slug
    
    # Direct match
    if pn == fs or pn in fs or fs in pn:
        return True
    
    # First/last name match
    pn_parts = pn.split('-')
    fs_parts = fs.split('-')
    
    if len(pn_parts) >= 1 and len(fs_parts) >= 1:
        # First name match
        if pn_parts[0] == fs_parts[0]:
            return True
        # Last name match
        if pn_parts[-1] == fs_parts[-1]:
            return True
        # Any significant part match
        for pp in pn_parts:
            if len(pp) > 3:
                for fp in fs_parts:
                    if pp == fp:
                        return True
    return False

def main():
    # Get all photos
    photos = list(PHOTOS_DIR.glob('*'))
    print(f"Found {len(photos)} photos in people_photos/")
    
    # Get all new person markdown files (untracked in git)
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True, cwd=ROOT)
    new_files = []
    for line in result.stdout.strip().split('\n'):
        if line.startswith('??') and '_people/alumni' in line and line.endswith('.md'):
            new_files.append(ROOT / line.split()[-1])
    
    print(f"Found {len(new_files)} new person files to process")
    
    # Match photos to people
    matched = []
    used_photos = set()
    
    for nf in new_files:
        nf_slug = nf.stem
        for photo in photos:
            if photo in used_photos:
                continue
            name = extract_name_from_photo(photo.name)
            if not name:
                continue
            if names_match(name, nf_slug):
                matched.append((photo, nf, name))
                used_photos.add(photo)
                break
    
    print(f"\nMatched {len(matched)} photos to profiles:")
    
    for photo, md_path, name in matched:
        print(f"\n  Processing: {name}")
        print(f"    Photo: {photo.name}")
        print(f"    Profile: {md_path.relative_to(ROOT)}")
        
        # Determine destination folder from md path
        # e.g., _people/alumni/phd-graduates/2021/person.md -> assets/img/people/alumni/phd/2021/
        parts = md_path.relative_to(ROOT / '_people' / 'alumni').parts
        category = parts[0]  # e.g., phd-graduates
        year = parts[1] if len(parts) > 2 else 'unknown'
        
        # Map category to img folder
        cat_map = {
            'phd-graduates': 'phd',
            'mtech-graduates': 'mtech',
            'mtech-research-graduates': 'mtech-research',
            'research-associates': 'research-associates',
            'interns': 'interns',
        }
        img_cat = cat_map.get(category, category)
        
        # Output path
        out_name = md_path.stem + '.jpg'
        out_dir = ASSETS_IMG / img_cat / year
        out_path = out_dir / out_name
        
        # Make square and save
        try:
            make_square_crop(photo, out_path)
            print(f"    Created: {out_path.relative_to(ROOT)}")
        except Exception as e:
            print(f"    ERROR making square: {e}")
            continue
        
        # Update markdown
        img_rel = f"assets/img/people/alumni/{img_cat}/{year}/{out_name}"
        update_md_img(md_path, img_rel)
        print(f"    Updated img in markdown")
    
    print(f"\n\nDone! Processed {len(matched)} photos.")
    
    # Show unmatched new files
    matched_mds = {m[1] for m in matched}
    unmatched = [nf for nf in new_files if nf not in matched_mds]
    if unmatched:
        print(f"\nProfiles without photos ({len(unmatched)}):")
        for u in unmatched:
            print(f"  - {u.relative_to(ROOT)}")

if __name__ == '__main__':
    main()
