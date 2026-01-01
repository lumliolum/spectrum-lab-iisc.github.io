#!/usr/bin/env python3
"""
People Profile Updater Script

This script automates updating people profiles from a Google Sheets CSV form.
It handles:
1. Downloading CSV data from Google Sheets
2. Downloading photos from Google Drive
3. Creating/updating profile markdown files
4. Processing images to square format

Usage:
    python update_people.py

Requirements:
    pip install gdown pandas pyyaml

Configuration:
    Update SHEET_ID and PHOTOS_FOLDER_ID below with your Google resource IDs.
"""

import os
import re
import subprocess
import sys
from pathlib import Path

# Try to import required packages
try:
    import pandas as pd
    import yaml
except ImportError:
    print("Installing required packages...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pandas", "pyyaml", "gdown"], check=True)
    import pandas as pd
    import yaml

# ============== CONFIGURATION ==============
SHEET_ID = "1_m83EXeUr0ZboZrWPEpjB6lAzSxVIq0XyugKENt72nQ"
PHOTOS_FOLDER_ID = "1-qqMJcdzORG0ncGZQ8JyV-fpV-5rSgZPQ9jYJo3vmKs7CqIsd0TXm_Lefi9utJl4RMavdbnX"

# Repository paths (adjust if needed)
REPO_ROOT = Path(__file__).parent.parent
PEOPLE_DIR = REPO_ROOT / "_people"
ASSETS_DIR = REPO_ROOT / "assets/img/people"
EMAILS_FILE = REPO_ROOT / "_data/emails.yml"

# Image processing settings
TARGET_IMAGE_SIZE = 400

# Category mappings
CATEGORY_MAP = {
    "PhD": {
        "category": "PhD Graduates",
        "description": "PhD",
        "path": "alumni/phd-graduates",
        "assets_path": "alumni/phd"
    },
    "M.Tech (Previously M.E.)": {
        "category": "M.Tech Graduates", 
        "description": "M.Tech",
        "path": "alumni/mtech-graduates",
        "assets_path": "alumni/mtech"
    },
    "M.Tech Research": {
        "category": "M.Tech Research Graduates",
        "description": "M.Tech Research Graduate",
        "path": "alumni/mtech-research-graduates",
        "assets_path": "alumni/mtech-research"
    },
    "Project Associate/ Research Associate": {
        "category": "Project Associates",
        "description": "Project Associate/Research Associate",
        "path": "alumni/project-associates",
        "assets_path": "alumni/project-associates"
    }
}


def download_csv():
    """Download CSV from Google Sheets."""
    print("📥 Downloading CSV from Google Sheets...")
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
    
    import urllib.request
    csv_path = REPO_ROOT / "temp_people_data.csv"
    
    try:
        urllib.request.urlretrieve(url, csv_path)
        print(f"   ✓ Downloaded to {csv_path}")
        return csv_path
    except Exception as e:
        print(f"   ✗ Failed to download CSV: {e}")
        print("   Note: The sheet must be publicly accessible or use gdown with auth")
        return None


def download_photos():
    """Download photos from Google Drive folder."""
    print("\n📸 Downloading photos from Google Drive...")
    photos_dir = REPO_ROOT / "temp_photos"
    photos_dir.mkdir(exist_ok=True)
    
    try:
        import gdown
        url = f"https://drive.google.com/drive/folders/{PHOTOS_FOLDER_ID}"
        gdown.download_folder(url, output=str(photos_dir), quiet=False)
        
        # Find the actual subfolder (Drive creates nested folder)
        for item in photos_dir.iterdir():
            if item.is_dir():
                return item
        return photos_dir
    except Exception as e:
        print(f"   ✗ Failed to download photos: {e}")
        return None


def extract_drive_id(url):
    """Extract file ID from Google Drive URL."""
    if not url or not isinstance(url, str):
        return None
    match = re.search(r'id=([a-zA-Z0-9_-]+)', url)
    return match.group(1) if match else None


def slugify(name):
    """Convert name to filename-friendly slug."""
    slug = name.lower().strip()
    slug = re.sub(r'[^a-z0-9]+', '_', slug)
    slug = slug.strip('_')
    return slug


def process_image(src_path, dst_path, method='center'):
    """
    Process image to square format.
    
    Args:
        src_path: Source image path
        dst_path: Destination path
        method: 'center' (crop from center), 'north' (crop from top), 'pad' (add padding)
    """
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    
    if method == 'pad':
        # Pad to square (preserves entire image)
        cmd = f'magick "{src_path}" -gravity center -background white -extent "%[fx:max(w,h)]x%[fx:max(w,h)]" -resize {TARGET_IMAGE_SIZE}x{TARGET_IMAGE_SIZE} "{dst_path}"'
    elif method == 'north':
        # Crop from top (for portraits where face is at top)
        cmd = f'magick "{src_path}" -gravity North -crop "%[fx:min(w,h)]x%[fx:min(w,h)]+0+0" +repage -resize {TARGET_IMAGE_SIZE}x{TARGET_IMAGE_SIZE} "{dst_path}"'
    else:
        # Center crop (default)
        cmd = f'magick "{src_path}" -gravity center -crop "%[fx:min(w,h)]x%[fx:min(w,h)]+0+0" +repage -resize {TARGET_IMAGE_SIZE}x{TARGET_IMAGE_SIZE} "{dst_path}"'
    
    try:
        subprocess.run(cmd, shell=True, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ✗ Failed to process image: {e}")
        return False


def create_profile(row, photos_dir):
    """Create or update a profile markdown file."""
    name = row.get('Full Name', '').strip()
    if not name:
        return None
    
    # Parse data
    email = row.get('Your Current Email Address', '').strip()
    bio = row.get('Your Brief Biography (About 200 words)', '').strip()
    position = row.get('What is your current professional role/affiliation?', '').strip()
    website = row.get('Your Website URL (Optional)', '').strip()
    linkedin = row.get('Social Media Handle URL (e.g., LinkedIn, Twitter, etc.) (Optional)', '').strip()
    scholar = row.get('Google Scholar Profile URL (Optional)', '').strip()
    year = str(row.get('Year of Graduation (From this lab/program)', '')).strip()
    grad_type = row.get('Graduated as:', '').strip()
    
    # Get category info
    cat_info = CATEGORY_MAP.get(grad_type)
    if not cat_info:
        print(f"   ⚠ Unknown graduation type for {name}: {grad_type}")
        return None
    
    # Extract year (handle formats like "2017, Spectrum Lab, PhD")
    year_match = re.search(r'20\d{2}', year)
    year = year_match.group(0) if year_match else year
    
    # Create filename
    filename = slugify(name) + ".md"
    
    # Determine profile path
    if "project-associates" in cat_info['path']:
        profile_dir = PEOPLE_DIR / cat_info['path']
    else:
        profile_dir = PEOPLE_DIR / cat_info['path'] / year
    
    profile_dir.mkdir(parents=True, exist_ok=True)
    profile_path = profile_dir / filename
    
    # Parse name parts
    name_parts = name.split()
    firstname = ' '.join(name_parts[:-1]) if len(name_parts) > 1 else name_parts[0]
    lastname = name_parts[-1] if len(name_parts) > 1 else ''
    
    # Extract LinkedIn username
    linkedin_username = ''
    if linkedin:
        match = re.search(r'linkedin\.com/in/([^/?]+)', linkedin)
        if match:
            linkedin_username = match.group(1)
    
    # Extract Scholar user ID
    scholar_userid = ''
    if scholar:
        match = re.search(r'user=([^&]+)', scholar)
        if match:
            scholar_userid = match.group(1)
    
    # Find matching photo
    photo_path = None
    img_field = ''
    if photos_dir:
        for photo_file in photos_dir.iterdir():
            if name.lower().split()[-1] in photo_file.name.lower():
                # Determine destination path
                if "project-associates" in cat_info['assets_path']:
                    img_dest = ASSETS_DIR / cat_info['assets_path'] / f"{slugify(name)}.jpg"
                else:
                    img_dest = ASSETS_DIR / cat_info['assets_path'] / year / f"{slugify(name)}.jpg"
                
                if process_image(photo_file, img_dest):
                    img_field = str(img_dest.relative_to(REPO_ROOT))
                break
    
    # Build biography paragraphs
    bio_paragraphs = []
    if bio:
        # Split on double newlines or long single paragraphs
        paragraphs = re.split(r'\n\n+', bio)
        bio_paragraphs = [p.strip().replace('"', "'") for p in paragraphs if p.strip()]
    
    # Build frontmatter
    frontmatter = {
        'layout': 'person',
        'title': name,
        'firstname': firstname,
        'lastname': lastname,
        'description': cat_info['description'],
        'category': cat_info['category'],
        'show': True,
        'year': int(year) if year.isdigit() else year,
        'email': email,
    }
    
    if img_field:
        frontmatter['img'] = img_field
    if website:
        frontmatter['website'] = website
    if linkedin_username:
        frontmatter['linkedin_username'] = linkedin_username
    if scholar_userid:
        frontmatter['scholar_userid'] = scholar_userid
    if position:
        frontmatter['current_position'] = position
    if bio_paragraphs:
        frontmatter['biography_paragraphs'] = bio_paragraphs
    
    # Write profile
    with open(profile_path, 'w') as f:
        f.write('---\n')
        yaml.dump(frontmatter, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        f.write('---\n')
    
    print(f"   ✓ Created/Updated: {profile_path.relative_to(REPO_ROOT)}")
    return profile_path


def update_emails(df):
    """Update emails.yml with new email addresses."""
    print("\n📧 Updating emails.yml...")
    
    if not EMAILS_FILE.exists():
        print("   ⚠ emails.yml not found")
        return
    
    with open(EMAILS_FILE, 'r') as f:
        emails = yaml.safe_load(f) or {}
    
    for _, row in df.iterrows():
        name = row.get('Full Name', '').strip()
        email = row.get('Your Current Email Address', '').strip()
        
        if name and email:
            key = slugify(name)
            if key not in emails or emails[key].endswith('@placeholder.com'):
                emails[key] = email
                print(f"   ✓ Added: {key}")
    
    with open(EMAILS_FILE, 'w') as f:
        yaml.dump(emails, f, default_flow_style=False, allow_unicode=True)


def cleanup():
    """Remove temporary files."""
    print("\n🧹 Cleaning up...")
    import shutil
    
    temp_csv = REPO_ROOT / "temp_people_data.csv"
    temp_photos = REPO_ROOT / "temp_photos"
    
    if temp_csv.exists():
        temp_csv.unlink()
    if temp_photos.exists():
        shutil.rmtree(temp_photos)
    
    print("   ✓ Cleaned up temporary files")


def main():
    print("=" * 60)
    print("🔄 People Profile Updater")
    print("=" * 60)
    
    # Download CSV
    csv_path = download_csv()
    if not csv_path or not csv_path.exists():
        print("\n❌ Failed to download CSV. Exiting.")
        return 1
    
    # Load CSV
    df = pd.read_csv(csv_path)
    print(f"\n📊 Loaded {len(df)} records from CSV")
    
    # Download photos
    photos_dir = download_photos()
    if photos_dir:
        print(f"   ✓ Photos downloaded to {photos_dir}")
    
    # Process each row
    print("\n👤 Processing profiles...")
    for _, row in df.iterrows():
        create_profile(row, photos_dir)
    
    # Update emails
    update_emails(df)
    
    # Cleanup
    cleanup()
    
    print("\n" + "=" * 60)
    print("✅ Done! Run 'bundle exec jekyll serve' to preview changes.")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
