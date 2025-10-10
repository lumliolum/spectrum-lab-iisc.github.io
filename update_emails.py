#!/usr/bin/env python3
"""
Update all BibTeX entries to have emails = {css@iisc.ac.in}
Replaces any existing emails fields with the standard one.
"""

import re

def process_bibtex_file(filepath):
    """Process BibTeX file and update emails fields."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into entries - find all @type{key, ... }
    # We'll process entry by entry
    entries = []
    current_pos = 0
    
    # Find all BibTeX entry starts
    entry_pattern = re.compile(r'(@\w+\{[^,]+,)', re.MULTILINE)
    
    lines = content.split('\n')
    result_lines = []
    in_entry = False
    entry_lines = []
    brace_count = 0
    
    for line in lines:
        if not in_entry:
            # Check if this line starts a new entry
            if re.match(r'^\s*@\w+\{', line):
                in_entry = True
                entry_lines = [line]
                brace_count = line.count('{') - line.count('}')
            else:
                result_lines.append(line)
        else:
            entry_lines.append(line)
            brace_count += line.count('{') - line.count('}')
            
            # Check if entry is complete
            if brace_count == 0:
                # Process this complete entry
                processed_entry = process_entry(entry_lines)
                result_lines.extend(processed_entry)
                in_entry = False
                entry_lines = []
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(result_lines))
    
    print(f"✅ Updated {filepath}")

def process_entry(entry_lines):
    """Process a single BibTeX entry to add/replace emails field."""
    # Check if emails field exists
    has_emails = False
    emails_line_idx = -1
    
    for idx, line in enumerate(entry_lines):
        if re.match(r'\s*emails\s*=', line):
            has_emails = True
            emails_line_idx = idx
            break
    
    if has_emails:
        # Replace existing emails field
        # entry_lines[emails_line_idx] = '  emails = {css@iisc.ac.in}'
        pass
    else:
        # Add emails field before the closing brace
        # Find the last field (before closing brace)
        closing_brace_idx = -1
        for idx in range(len(entry_lines) - 1, -1, -1):
            if '}' in entry_lines[idx] and not entry_lines[idx].strip().startswith('%'):
                closing_brace_idx = idx
                break
        
        if closing_brace_idx > 0:
            # Ensure the previous line has a comma if it's a field
            prev_idx = closing_brace_idx - 1
            if prev_idx >= 0 and not entry_lines[prev_idx].strip().startswith('%'):
                if not entry_lines[prev_idx].strip().endswith(','):
                    entry_lines[prev_idx] = entry_lines[prev_idx].rstrip() + ','
            # Insert before closing brace
            entry_lines.insert(closing_brace_idx, '  emails = {css@iisc.ac.in}')
    
    return entry_lines

if __name__ == '__main__':
    filepath = '/Users/gourishanker/spectrum-lab-iisc.github.io/_bibliography/papers.bib'
    process_bibtex_file(filepath)
    print("Done!")
