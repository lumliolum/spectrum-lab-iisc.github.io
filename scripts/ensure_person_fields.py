#!/usr/bin/env python3
"""
Script to automatically fill in missing email and alias fields in person markdown files.
Run this before Jekyll build to ensure all person profiles have required fields.

Usage:
    python scripts/ensure_person_fields.py

This script will:
1. Scan all .md files in _people/ directory
2. For files with 'layout: person' that are missing email or alias:
   - Generate a placeholder email if missing
   - Generate a unique alias from the filename if missing
3. Update the files in place
"""

import os
import re
import sys
from pathlib import Path

PEOPLE_DIR = Path(__file__).parent.parent / "_people"
SKIP_FILES = {"TEMPLATE_README.md", "person_template.md", "UPDATE_LOG.md"}


def get_existing_aliases(people_dir: Path) -> set:
    """Collect all existing aliases to ensure uniqueness."""
    aliases = set()
    for md_file in people_dir.rglob("*.md"):
        if md_file.name in SKIP_FILES:
            continue
        try:
            content = md_file.read_text()
            match = re.search(r'^alias:\s*(.+)$', content, re.MULTILINE)
            if match:
                aliases.add(match.group(1).strip())
        except Exception:
            pass
    return aliases


def generate_alias_from_filename(filename: str, existing_aliases: set) -> str:
    """Generate a unique alias from the filename."""
    # Remove .md extension and convert to lowercase
    base = filename.replace(".md", "").lower()
    
    # Replace hyphens and spaces with underscores
    alias = re.sub(r'[-\s]+', '_', base)
    
    # Remove any non-alphanumeric characters except underscores
    alias = re.sub(r'[^a-z0-9_]', '', alias)
    
    # Ensure uniqueness
    original_alias = alias
    counter = 1
    while alias in existing_aliases:
        alias = f"{original_alias}_{counter}"
        counter += 1
    
    return alias


def generate_placeholder_email(firstname: str, lastname: str) -> str:
    """Generate a placeholder email from name."""
    first = re.sub(r'[^a-z]', '', firstname.lower()) if firstname else "user"
    last = re.sub(r'[^a-z]', '', lastname.lower()) if lastname else ""
    
    if last:
        return f"{first}{last[0]}@placeholder.iisc.ac.in"
    return f"{first}@placeholder.iisc.ac.in"


def extract_frontmatter_field(content: str, field: str) -> str:
    """Extract a field value from YAML frontmatter."""
    match = re.search(rf'^{field}:\s*(.+)$', content, re.MULTILINE)
    if match:
        value = match.group(1).strip()
        # Remove quotes if present
        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]
        return value
    return ""


def process_file(md_file: Path, existing_aliases: set, dry_run: bool = False) -> tuple:
    """Process a single markdown file and add missing fields."""
    content = md_file.read_text()
    
    # Only process person layout files
    if 'layout: person' not in content:
        return None, None
    
    modified = False
    added_email = None
    added_alias = None
    
    # Check for email field
    has_email = bool(re.search(r'^email:\s*\S+', content, re.MULTILINE))
    
    # Check for alias field
    has_alias = bool(re.search(r'^alias:\s*\S+', content, re.MULTILINE))
    
    if has_email and has_alias:
        return None, None  # Already has both fields
    
    # Extract name fields for email generation
    firstname = extract_frontmatter_field(content, 'firstname')
    lastname = extract_frontmatter_field(content, 'lastname')
    
    # Add missing email
    if not has_email:
        new_email = generate_placeholder_email(firstname, lastname)
        # Insert after lastname field or title field
        if lastname:
            content = re.sub(
                r'(lastname:\s*.+\n)',
                f'\\1email: {new_email}\n',
                content
            )
        else:
            content = re.sub(
                r'(title:\s*.+\n)',
                f'\\1email: {new_email}\n',
                content
            )
        added_email = new_email
        modified = True
    
    # Add missing alias
    if not has_alias:
        new_alias = generate_alias_from_filename(md_file.name, existing_aliases)
        existing_aliases.add(new_alias)  # Track for uniqueness
        
        # Insert after email field
        if re.search(r'^email:\s*', content, re.MULTILINE):
            content = re.sub(
                r'(email:\s*.+\n)',
                f'\\1alias: {new_alias}\n',
                content
            )
        else:
            # Insert after lastname or title
            if lastname:
                content = re.sub(
                    r'(lastname:\s*.+\n)',
                    f'\\1alias: {new_alias}\n',
                    content
                )
            else:
                content = re.sub(
                    r'(title:\s*.+\n)',
                    f'\\1alias: {new_alias}\n',
                    content
                )
        added_alias = new_alias
        modified = True
    
    if modified and not dry_run:
        md_file.write_text(content)
    
    return added_email, added_alias


def main():
    """Main function to process all person files."""
    dry_run = "--dry-run" in sys.argv
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    
    if not PEOPLE_DIR.exists():
        print(f"Error: People directory not found: {PEOPLE_DIR}")
        sys.exit(1)
    
    print("🔍 Scanning person profiles for missing email/alias fields...")
    print(f"   Directory: {PEOPLE_DIR}")
    if dry_run:
        print("   Mode: DRY RUN (no files will be modified)")
    print()
    
    # Collect existing aliases first
    existing_aliases = get_existing_aliases(PEOPLE_DIR)
    print(f"   Found {len(existing_aliases)} existing aliases")
    print()
    
    # Process all files
    updated_count = 0
    for md_file in sorted(PEOPLE_DIR.rglob("*.md")):
        if md_file.name in SKIP_FILES:
            continue
        
        try:
            added_email, added_alias = process_file(md_file, existing_aliases, dry_run)
            
            if added_email or added_alias:
                updated_count += 1
                rel_path = md_file.relative_to(PEOPLE_DIR)
                print(f"{'[DRY RUN] ' if dry_run else ''}Updated: {rel_path}")
                if added_email:
                    print(f"   + email: {added_email}")
                if added_alias:
                    print(f"   + alias: {added_alias}")
            elif verbose:
                rel_path = md_file.relative_to(PEOPLE_DIR)
                print(f"   OK: {rel_path}")
                
        except Exception as e:
            print(f"   Error processing {md_file.name}: {e}")
    
    print()
    if updated_count > 0:
        action = "would be updated" if dry_run else "updated"
        print(f"✅ {updated_count} file(s) {action}")
    else:
        print("✅ All person profiles already have email and alias fields")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
