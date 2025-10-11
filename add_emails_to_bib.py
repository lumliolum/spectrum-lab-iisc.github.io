#!/usr/bin/env python3
"""
Script to add email entries to bibliography entries based on people in _people directory
"""

import os
import re
import yaml
from pathlib import Path

def extract_people_emails():
    """Extract name-email mappings from _people directory"""
    people_dir = Path("_people")
    email_mappings = {}
    
    for md_file in people_dir.glob("*.md"):
        if md_file.name in ["person_template.md", "TEMPLATE_README.md"]:
            continue
            
        try:
            content = md_file.read_text(encoding='utf-8')
            # Extract YAML front matter
            if content.startswith('---\n'):
                end_marker = content.find('\n---\n', 4)
                if end_marker != -1:
                    yaml_content = content[4:end_marker]
                    data = yaml.safe_load(yaml_content)
                    
                    if 'email' in data and 'firstname' in data and 'lastname' in data:
                        # Create various name formats for matching
                        firstname = data['firstname'].strip()
                        lastname = data['lastname'].strip()
                        email = data['email'].strip()
                        
                        # Store different name variations
                        variations = [
                            f"{lastname}, {firstname}",
                            f"{firstname} {lastname}",
                            f"{lastname}, {firstname[0]}.",
                            f"{firstname[0]}. {lastname}",
                        ]
                        
                        # Handle middle names/initials
                        if ' ' in firstname:
                            parts = firstname.split()
                            first_part = parts[0]
                            variations.extend([
                                f"{lastname}, {first_part}",
                                f"{first_part} {lastname}",
                                f"{lastname}, {first_part[0]}.",
                                f"{first_part[0]}. {lastname}",
                            ])
                        
                        for variation in variations:
                            email_mappings[variation.lower()] = email
                            
        except Exception as e:
            print(f"Error processing {md_file}: {e}")
    
    return email_mappings

def process_bibliography():
    """Process the bibliography file and add emails"""
    bib_file = Path("_bibliography/papers.bib")
    
    if not bib_file.exists():
        print("Bibliography file not found!")
        return
    
    # Get email mappings
    email_mappings = extract_people_emails()
    print(f"Found {len(email_mappings)} email mappings")
    
    # Read bibliography content
    content = bib_file.read_text(encoding='utf-8')
    
    # Process each entry
    entries = re.findall(r'@\w+\{[^,]+,.*?\n\}', content, re.DOTALL)
    
    modified_content = content
    
    for entry in entries:
        # Extract year
        year_match = re.search(r'year\s*=\s*[{"]?(\d{4})[}"]?', entry)
        if not year_match:
            continue
            
        year = int(year_match.group(1))
        if year < 2019 or year > 2025:
            continue
        
        # Check if already has emails field
        if 'emails' in entry.lower():
            continue
            
        # Extract authors
        author_match = re.search(r'author\s*=\s*[{"]([^}]+)[}"]', entry)
        if not author_match:
            continue
            
        authors_str = author_match.group(1)
        authors = [author.strip() for author in authors_str.split(' and ')]
        
        # Find emails for authors
        found_emails = []
        for author in authors:
            author_clean = re.sub(r'[{}]', '', author).strip()
            if author_clean.lower() in email_mappings:
                found_emails.append(email_mappings[author_clean.lower()])
        
        # Add emails field if any emails found
        if found_emails:
            emails_str = f"emails = {{{', '.join(found_emails)}}}"
            
            # Find the position to insert (before the closing brace)
            entry_end = entry.rfind('}')
            if entry_end != -1:
                # Check if there's already a trailing comma or field before the closing brace
                before_brace = entry[:entry_end].rstrip()
                if not before_brace.endswith(','):
                    emails_str = f",\n  {emails_str}"
                else:
                    emails_str = f"\n  {emails_str}"
                
                new_entry = entry[:entry_end] + emails_str + '\n' + entry[entry_end:]
                modified_content = modified_content.replace(entry, new_entry)
                
                print(f"Added emails to entry with authors: {authors_str}")
    
    # Write back the modified content
    bib_file.write_text(modified_content, encoding='utf-8')
    print("Bibliography updated successfully!")

if __name__ == "__main__":
    process_bibliography()