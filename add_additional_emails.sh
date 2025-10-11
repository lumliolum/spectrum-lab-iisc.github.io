#!/bin/bash

# Script to add additional email entries to papers.bib for specific authors
# Based on the manually provided author-email mappings

BIBLIOGRAPHY_FILE="/Users/abijithjkamath/spectrum-admin/spectrum-lab-iisc.github.io/_bibliography/papers.bib"

# Create another backup before making changes
cp "$BIBLIOGRAPHY_FILE" "${BIBLIOGRAPHY_FILE}.backup2"

echo "Adding emails for additional authors..."

# Create a Python script to process the bibliography
python3 << 'EOF'
import re
import sys

# Additional author mappings provided by the user
additional_mappings = {
    'Kamath, A. J.': 'abijithj@iisc.ac.in',
    'Bhandiwad, A. S.': 'abhishekbs@iisc.ac.in', 
    'Prabakar, A': 'pakash@iisc.ac.in'
}

# Read the bibliography file
with open('/Users/abijithjkamath/spectrum-admin/spectrum-lab-iisc.github.io/_bibliography/papers.bib', 'r') as f:
    content = f.read()

# Split into entries
entries = re.split(r'\n@', content)
modified_count = 0

new_content = []
for i, entry in enumerate(entries):
    if i == 0:
        entry_text = entry
    else:
        entry_text = '@' + entry
    
    # Skip if entry already has emails field
    if 'emails = {' in entry_text:
        new_content.append(entry_text)
        continue
    
    # Look for year to filter 2019-2025
    year_match = re.search(r'year\s*=\s*\{(\d{4})\}', entry_text)
    if not year_match:
        new_content.append(entry_text)
        continue
    
    year = int(year_match.group(1))
    if year < 2019 or year > 2025:
        new_content.append(entry_text)
        continue
    
    # Find author field
    author_match = re.search(r'author\s*=\s*\{([^}]+)\}', entry_text)
    if not author_match:
        new_content.append(entry_text)
        continue
    
    author_field = author_match.group(1)
    
    # Find matching emails for this entry
    matched_emails = []
    for author_pattern, email in additional_mappings.items():
        if author_pattern in author_field:
            matched_emails.append(email)
    
    if matched_emails:
        # Add emails field before the closing brace
        # Find the last field and add emails after it
        closing_brace_pos = entry_text.rfind('}')
        if closing_brace_pos != -1:
            # Insert emails field before the closing brace
            emails_str = ', '.join(matched_emails)
            emails_field = f",\n  emails = {{{emails_str}}}\n"
            modified_entry = entry_text[:closing_brace_pos] + emails_field + entry_text[closing_brace_pos:]
            new_content.append(modified_entry)
            modified_count += 1
            print(f"Added emails for: {', '.join([author for author in additional_mappings.keys() if author in author_field])}")
        else:
            new_content.append(entry_text)
    else:
        new_content.append(entry_text)

# Write the modified content back
final_content = '\n'.join(new_content)
with open('/Users/abijithjkamath/spectrum-admin/spectrum-lab-iisc.github.io/_bibliography/papers.bib', 'w') as f:
    f.write(final_content)

print(f"\nProcessing complete. Modified {modified_count} entries with additional emails.")
EOF

echo "Script completed!"