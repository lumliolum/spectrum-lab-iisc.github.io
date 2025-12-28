import os
import yaml
import re

# Configuration
PEOPLE_DIR = '_people/alumni'
EMAILS_FILE = '_data/emails.yml'
CATEGORIES = ['phd-graduates', 'mtech-graduates', 'mtech-research-graduates']
PLACEHOLDER_DOMAIN = 'placeholder.com'

def load_emails():
    if os.path.exists(EMAILS_FILE):
        with open(EMAILS_FILE, 'r') as f:
            return yaml.safe_load(f) or {}
    return {}

def save_emails(emails_data):
    # Sort keys to keep file organized
    # We want to keep comments if possible, but PyYAML doesn't preserve them easily.
    # For now, we'll append new entries to the end or rewrite.
    # Since we want to preserve the structure (Lab Director, Current Members, etc.),
    # we'll read the file as text and append new entries if they don't exist.
    
    # Actually, let's just read the existing keys to check for duplicates
    # and append new ones to the end of the file as text.
    pass

def append_email_to_file(alias, email):
    with open(EMAILS_FILE, 'a') as f:
        f.write(f"{alias}: {email}\n")

def process_alumni():
    existing_emails_data = load_emails()
    existing_emails = set(existing_emails_data.values())
    existing_aliases = set(existing_emails_data.keys())
    
    # We need to track what we've added in this run to avoid duplicates
    new_aliases = {}

    for category in CATEGORIES:
        dir_path = os.path.join(PEOPLE_DIR, category)
        if not os.path.exists(dir_path):
            continue
            
        print(f"Processing {category}...")
        
        for filename in os.listdir(dir_path):
            if not filename.endswith('.md'):
                continue
                
            file_path = os.path.join(dir_path, filename)
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Parse frontmatter
            frontmatter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
            if not frontmatter_match:
                print(f"Skipping {filename}: No frontmatter found")
                continue
                
            frontmatter_text = frontmatter_match.group(1)
            try:
                frontmatter = yaml.safe_load(frontmatter_text)
            except yaml.YAMLError as e:
                print(f"Skipping {filename}: YAML error {e}")
                continue
            
            firstname = frontmatter.get('firstname', '').strip()
            lastname = frontmatter.get('lastname', '').strip()
            
            if not firstname:
                print(f"Skipping {filename}: No firstname")
                continue

            # Generate alias
            alias_base = f"{firstname.lower()}_{lastname.lower()}" if lastname else firstname.lower()
            # Remove special chars from alias
            alias = re.sub(r'[^a-z0-9_]', '', alias_base)
            
            email = frontmatter.get('email')
            
            if email:
                # Email exists in file
                if email not in existing_emails:
                    # Check if alias exists
                    if alias in existing_aliases:
                        # Append a number if alias exists
                        counter = 2
                        while f"{alias}{counter}" in existing_aliases:
                            counter += 1
                        alias = f"{alias}{counter}"
                    
                    print(f"Adding existing email: {alias} -> {email}")
                    append_email_to_file(alias, email)
                    existing_emails.add(email)
                    existing_aliases.add(alias)
            else:
                # Email missing, generate dummy
                dummy_email = f"{firstname.lower()}.{lastname.lower()}@{PLACEHOLDER_DOMAIN}"
                
                # Check if this dummy email was already added (unlikely but possible)
                if dummy_email not in existing_emails:
                     # Check if alias exists
                    if alias in existing_aliases:
                        counter = 2
                        while f"{alias}{counter}" in existing_aliases:
                            counter += 1
                        alias = f"{alias}{counter}"
                        
                    print(f"Adding dummy email: {alias} -> {dummy_email}")
                    append_email_to_file(alias, dummy_email)
                    existing_emails.add(dummy_email)
                    existing_aliases.add(alias)
                    
                    # Update markdown file
                    new_frontmatter_text = frontmatter_text + f"\nemail: {dummy_email}"
                    new_content = content.replace(frontmatter_text, new_frontmatter_text)
                    
                    with open(file_path, 'w') as f:
                        f.write(new_content)
                    print(f"Updated {filename} with dummy email")

if __name__ == "__main__":
    # Add a header for new entries if not present
    with open(EMAILS_FILE, 'r') as f:
        content = f.read()
    
    if "# Auto-generated Alumni Emails" not in content:
        with open(EMAILS_FILE, 'a') as f:
            f.write("\n\n# Auto-generated Alumni Emails\n")
            
    process_alumni()
