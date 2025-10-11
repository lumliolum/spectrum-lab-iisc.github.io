#!/bin/bash

# Create a temporary file to store name-email mappings
MAPPING_FILE="/tmp/name_email_mapping.txt"

# Extract name-email mappings from _people directory
echo "Extracting name-email mappings..."
> "$MAPPING_FILE"

for file in _people/*.md; do
    if [[ "$file" == *"template"* ]] || [[ "$file" == *"README"* ]]; then
        continue
    fi
    
    # Extract firstname, lastname, and email from YAML front matter
    firstname=$(grep "^firstname:" "$file" | sed 's/firstname: *//' | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')
    lastname=$(grep "^lastname:" "$file" | sed 's/lastname: *//' | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')
    email=$(grep "^email:" "$file" | sed 's/email: *//' | sed 's/^[[:space:]]*//' | sed 's/[[:space:]]*$//')
    
    if [[ -n "$firstname" && -n "$lastname" && -n "$email" ]]; then
        # Create various name formats
        echo "$lastname, $firstname|$email" >> "$MAPPING_FILE"
        echo "$firstname $lastname|$email" >> "$MAPPING_FILE"
        
        # Handle first initial
        first_initial=${firstname:0:1}
        echo "$lastname, $first_initial.|$email" >> "$MAPPING_FILE"
        echo "$first_initial. $lastname|$email" >> "$MAPPING_FILE"
        
        # Handle middle names
        if [[ "$firstname" == *" "* ]]; then
            first_part=$(echo "$firstname" | cut -d' ' -f1)
            echo "$lastname, $first_part|$email" >> "$MAPPING_FILE"
            echo "$first_part $lastname|$email" >> "$MAPPING_FILE"
            first_part_initial=${first_part:0:1}
            echo "$lastname, $first_part_initial.|$email" >> "$MAPPING_FILE"
            echo "$first_part_initial. $lastname|$email" >> "$MAPPING_FILE"
        fi
    fi
done

echo "Found $(wc -l < "$MAPPING_FILE") name variations"

# Create backup of bibliography
cp _bibliography/papers.bib _bibliography/papers.bib.backup

# Process bibliography entries from 2019-2025
echo "Processing bibliography entries..."

# Create a temporary script to process the bibliography
cat > /tmp/process_bib.py << 'EOF'
import re
import sys

def main():
    mapping_file = "/tmp/name_email_mapping.txt"
    
    # Read email mappings
    email_mappings = {}
    try:
        with open(mapping_file, 'r') as f:
            for line in f:
                if '|' in line:
                    name, email = line.strip().split('|', 1)
                    email_mappings[name.lower()] = email
    except FileNotFoundError:
        print("Mapping file not found!")
        return
    
    # Read bibliography
    with open('_bibliography/papers.bib', 'r') as f:
        content = f.read()
    
    # Find all entries
    entries = re.findall(r'(@\w+\{[^,]+,.*?\n\})', content, re.DOTALL)
    
    modified_content = content
    changes_made = 0
    
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
            emails_str = f"  emails = {{{', '.join(found_emails)}}}"
            
            # Find the position to insert (before the closing brace)
            entry_lines = entry.split('\n')
            new_entry_lines = []
            
            for i, line in enumerate(entry_lines):
                new_entry_lines.append(line)
                # Insert emails before the closing brace line
                if i == len(entry_lines) - 2:  # Before the last line which should be '}'
                    if not line.strip().endswith(','):
                        new_entry_lines[-1] = line.rstrip() + ','
                    new_entry_lines.append(emails_str)
            
            new_entry = '\n'.join(new_entry_lines)
            modified_content = modified_content.replace(entry, new_entry)
            changes_made += 1
            
            print(f"Added emails to entry: {authors_str[:50]}...")
    
    # Write back the modified content
    with open('_bibliography/papers.bib', 'w') as f:
        f.write(modified_content)
    
    print(f"Bibliography updated! Made {changes_made} changes.")

if __name__ == "__main__":
    main()
EOF

python3 /tmp/process_bib.py

# Clean up
rm -f "$MAPPING_FILE" /tmp/process_bib.py

echo "Done!"