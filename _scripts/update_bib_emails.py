import os
import yaml
import re
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

# Configuration
EMAILS_FILE = '_data/emails.yml'
BIB_FILE = '_bibliography/papers.bib'
PEOPLE_DIR = '_people/alumni'
CATEGORIES = ['phd-graduates', 'mtech-graduates', 'mtech-research-graduates']

def load_emails():
    if os.path.exists(EMAILS_FILE):
        with open(EMAILS_FILE, 'r') as f:
            return yaml.safe_load(f) or {}
    return {}

def load_alumni_map(emails_data):
    """
    Returns a list of dicts: {'firstname': ..., 'lastname': ..., 'alias': ...}
    """
    alumni = []
    # Reverse lookup for alias -> email (not strictly needed if we trust the file structure)
    
    # We need to map Name -> Alias.
    # Since we generated aliases in the previous step, we can try to reconstruct/find them.
    # But the most reliable way is to read the markdown files again, generate the alias 
    # (or check if email matches one in emails.yml) and store the name.
    
    # Let's read the markdown files
    for category in CATEGORIES:
        dir_path = os.path.join(PEOPLE_DIR, category)
        if not os.path.exists(dir_path):
            continue
            
        for filename in os.listdir(dir_path):
            if not filename.endswith('.md'):
                continue
                
            file_path = os.path.join(dir_path, filename)
            with open(file_path, 'r') as f:
                content = f.read()
            
            frontmatter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
            if not frontmatter_match:
                continue
            
            try:
                frontmatter = yaml.safe_load(frontmatter_match.group(1))
            except:
                continue
                
            firstname = frontmatter.get('firstname', '').strip()
            lastname = frontmatter.get('lastname', '').strip()
            email = frontmatter.get('email', '').strip()
            
            if not firstname or not email:
                continue
                
            # Find alias for this email
            alias = None
            for k, v in emails_data.items():
                if v == email:
                    alias = k
                    break
            
            if alias:
                alumni.append({
                    'firstname': firstname,
                    'lastname': lastname,
                    'alias': alias
                })
    return alumni

def match_author(author_str, alumni_list):
    """
    Matches a BibTeX author string (e.g. "Seelamantula, C. S." or "Chandra Sekhar Seelamantula")
    to an alumnus.
    """
    # Normalize author string
    # BibTeX authors are usually "Last, First" or "First Last"
    parts = author_str.split(',')
    if len(parts) == 2:
        last = parts[0].strip()
        first = parts[1].strip()
    else:
        # Assume "First Last" - simplistic but often true if no comma
        parts = author_str.split(' ')
        last = parts[-1].strip()
        first = " ".join(parts[:-1]).strip()
        
    last_lower = last.lower()
    first_lower = first.lower()
    
    for alum in alumni_list:
        alum_last = alum['lastname'].lower()
        alum_first = alum['firstname'].lower()
        
        # Check Lastname match
        if last_lower != alum_last:
            continue
            
        # Check Firstname match
        # 1. Exact match
        if first_lower == alum_first:
            return alum['alias']
        
        # 2. Initial match (if bib has "S." and alum is "Sunil")
        # Remove dots from first name
        first_clean = first_lower.replace('.', ' ').strip()
        alum_first_clean = alum_first.replace('.', ' ').strip()
        
        # Check if first char matches
        if first_clean and alum_first_clean:
            if first_clean[0] == alum_first_clean[0]:
                # Weak match, but likely correct for this specific lab context
                # To be safer, maybe check if the first name is just an initial
                if len(first_clean) == 1 or (len(first_clean) > 1 and first_clean[1] == ' '):
                     return alum['alias']
                
                # If bib has full name "Sunil" and alum is "Sunil", matched above.
                # If bib has "Sunil" and alum is "S.", we can't be sure, but usually alum has full name.
                
    return None

def update_bib():
    emails_data = load_emails()
    alumni_list = load_alumni_map(emails_data)
    
    print(f"Loaded {len(alumni_list)} alumni records.")
    
    with open(BIB_FILE, 'r') as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    
    count = 0
    for entry in bib_database.entries:
        if 'author' not in entry:
            continue
            
        authors = entry['author'].split(' and ')
        matched_aliases = []
        
        # Get existing emails/aliases
        existing_emails_field = entry.get('emails', '')
        # Remove braces if present
        existing_emails_field = existing_emails_field.replace('{', '').replace('}', '')
        existing_list = [e.strip() for e in existing_emails_field.split(',') if e.strip()]
        
        # Check each author
        for author in authors:
            alias = match_author(author, alumni_list)
            if alias:
                if alias not in existing_list and alias not in matched_aliases:
                    matched_aliases.append(alias)
                    # print(f"Matched {author} -> {alias}")
        
        if matched_aliases:
            # Add new aliases to existing list
            existing_list.extend(matched_aliases)
            # Update entry
            new_emails_str = ", ".join(existing_list)
            # Wrap in braces if it wasn't empty or if we prefer that style
            # The original file had braces emails={...}
            entry['emails'] = "{" + new_emails_str + "}"
            count += 1
            
    print(f"Updated {count} entries.")
    
    # Save
    writer = BibTexWriter()
    writer.indent = '  '     # indent entries with 2 spaces
    writer.order_entries_by = None  # preserve order if possible, or 'ID'
    # Note: bibtexparser might reorder fields or entries. 
    # To minimize diff noise, we might want to be careful, but for now let's save.
    
    with open(BIB_FILE, 'w') as bibtex_file:
        bibtex_file.write(writer.write(bib_database))

if __name__ == "__main__":
    update_bib()
