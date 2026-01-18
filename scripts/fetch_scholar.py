#!/usr/bin/env python3
"""
Fetch publications from Google Scholar and update bibliography.

This script fetches publications from a Google Scholar author profile,
compares them against the existing papers.bib file, and outputs new
entries for review.

Usage:
    python fetch_scholar.py --dry-run      # Preview new entries
    python fetch_scholar.py --merge        # Append new entries to papers.bib
    python fetch_scholar.py --list-all     # List all publications from Scholar
"""

import argparse
import os
import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

try:
    from scholarly import scholarly
except ImportError:
    print("Error: 'scholarly' package not installed.")
    print("Install with: pip install scholarly")
    sys.exit(1)

try:
    import bibtexparser
    from bibtexparser.bwriter import BibTexWriter
    from bibtexparser.bibdatabase import BibDatabase
except ImportError:
    print("Error: 'bibtexparser' package not installed.")
    print("Install with: pip install bibtexparser")
    sys.exit(1)

try:
    from rapidfuzz import fuzz
except ImportError:
    try:
        from fuzzywuzzy import fuzz
    except ImportError:
        print("Error: Neither 'rapidfuzz' nor 'fuzzywuzzy' package installed.")
        print("Install with: pip install rapidfuzz")
        sys.exit(1)


# Configuration
SCHOLAR_ID = "1g1i1B4AAAAJ"  # Prof. Chandra Sekhar Seelamantula
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
BIB_FILE = PROJECT_ROOT / "_bibliography" / "papers.bib"
NEW_BIB_FILE = PROJECT_ROOT / "_bibliography" / "new_papers.bib"

# Rate limiting
REQUEST_DELAY = 2.0  # seconds between requests


def normalize_title(title: str) -> str:
    """Normalize title for comparison."""
    # Remove LaTeX commands, special chars, lowercase
    title = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', title)  # \command{text} -> text
    title = re.sub(r'[{}\\]', '', title)  # Remove braces and backslashes
    title = re.sub(r'[^a-zA-Z0-9\s]', '', title)  # Keep only alphanumeric
    title = title.lower().strip()
    title = re.sub(r'\s+', ' ', title)  # Normalize whitespace
    return title


def load_existing_titles(bib_path: Path) -> Set[str]:
    """Load normalized titles from existing BibTeX file."""
    if not bib_path.exists():
        return set()
    
    with open(bib_path, 'r', encoding='utf-8') as f:
        bib_database = bibtexparser.load(f)
    
    titles = set()
    for entry in bib_database.entries:
        if 'title' in entry:
            titles.add(normalize_title(entry['title']))
    
    return titles


def is_duplicate(title: str, existing_titles: Set[str], threshold: int = 85) -> bool:
    """Check if title matches any existing title using fuzzy matching."""
    normalized = normalize_title(title)
    
    for existing in existing_titles:
        similarity = fuzz.ratio(normalized, existing)
        if similarity >= threshold:
            return True
    
    return False


def generate_bibtex_key(pub: Dict) -> str:
    """Generate a BibTeX key from publication data."""
    # Get first author's last name
    authors = pub.get('bib', {}).get('author', 'unknown')
    if isinstance(authors, list):
        first_author = authors[0] if authors else 'unknown'
    else:
        first_author = authors.split(' and ')[0] if authors else 'unknown'
    
    # Extract last name
    parts = first_author.replace(',', '').split()
    last_name = parts[-1] if parts else 'unknown'
    last_name = re.sub(r'[^a-zA-Z]', '', last_name).lower()
    
    # Get year
    year = pub.get('bib', {}).get('pub_year', 'xxxx')
    
    # Get first significant word from title
    title = pub.get('bib', {}).get('title', '')
    words = re.findall(r'[a-zA-Z]+', title)
    # Skip common words
    skip_words = {'a', 'an', 'the', 'on', 'in', 'of', 'for', 'and', 'to', 'with'}
    title_word = next((w.lower() for w in words if w.lower() not in skip_words), 'paper')
    
    return f"{last_name}{year}{title_word}"


def pub_to_bibtex(pub: Dict) -> Optional[str]:
    """Convert a scholarly publication to BibTeX entry."""
    bib = pub.get('bib', {})
    
    if not bib.get('title'):
        return None
    
    # Determine entry type
    venue = bib.get('venue', '').lower()
    if 'conference' in venue or 'proceedings' in venue or 'icassp' in venue.lower():
        entry_type = 'inproceedings'
    elif 'journal' in venue or 'transactions' in venue:
        entry_type = 'article'
    elif 'arxiv' in venue.lower():
        entry_type = 'misc'
    else:
        entry_type = 'article'  # Default
    
    key = generate_bibtex_key(pub)
    
    # Build entry
    entry = BibDatabase()
    entry_dict = {
        'ENTRYTYPE': entry_type,
        'ID': key,
        'title': bib.get('title', ''),
        'author': bib.get('author', ''),
        'year': str(bib.get('pub_year', '')),
        'bibtex_show': 'true',
    }
    
    # Add venue-specific fields
    if entry_type == 'inproceedings':
        entry_dict['booktitle'] = bib.get('venue', '')
    elif entry_type == 'article':
        entry_dict['journal'] = bib.get('venue', '')
    
    # Add citation count as comment
    citations = pub.get('num_citations', 0)
    if citations > 0:
        entry_dict['note'] = f"Cited by {citations}"
    
    # Add URL if available
    if pub.get('pub_url'):
        entry_dict['url'] = pub.get('pub_url')
    
    entry.entries = [entry_dict]
    
    writer = BibTexWriter()
    writer.indent = '  '
    return writer.write(entry)


def fetch_publications(author_id: str, max_pubs: int = 500) -> List[Dict]:
    """Fetch publications from Google Scholar."""
    print(f"Fetching author profile for ID: {author_id}...")
    
    try:
        author = scholarly.search_author_id(author_id)
        author = scholarly.fill(author, sections=['publications'])
    except Exception as e:
        print(f"Error fetching author: {e}")
        return []
    
    publications = []
    pubs = author.get('publications', [])
    
    print(f"Found {len(pubs)} publications. Fetching details...")
    
    for i, pub in enumerate(pubs[:max_pubs]):
        try:
            # Rate limiting
            if i > 0:
                time.sleep(REQUEST_DELAY)
            
            # Fetch full publication details
            filled_pub = scholarly.fill(pub)
            publications.append(filled_pub)
            
            title = filled_pub.get('bib', {}).get('title', 'Unknown')[:50]
            print(f"  [{i+1}/{min(len(pubs), max_pubs)}] {title}...")
            
        except Exception as e:
            print(f"  Error fetching publication {i+1}: {e}")
            continue
    
    return publications


def main():
    parser = argparse.ArgumentParser(
        description="Fetch publications from Google Scholar"
    )
    parser.add_argument(
        '--dry-run', 
        action='store_true',
        help='Preview new entries without saving'
    )
    parser.add_argument(
        '--merge',
        action='store_true', 
        help='Append new entries to papers.bib'
    )
    parser.add_argument(
        '--list-all',
        action='store_true',
        help='List all publications from Scholar'
    )
    parser.add_argument(
        '--max-pubs',
        type=int,
        default=50,
        help='Maximum publications to fetch (default: 50)'
    )
    parser.add_argument(
        '--scholar-id',
        type=str,
        default=SCHOLAR_ID,
        help=f'Google Scholar author ID (default: {SCHOLAR_ID})'
    )
    
    args = parser.parse_args()
    
    # Load existing titles
    print(f"Loading existing bibliography from {BIB_FILE}...")
    existing_titles = load_existing_titles(BIB_FILE)
    print(f"Found {len(existing_titles)} existing entries.")
    
    # Fetch from Google Scholar
    publications = fetch_publications(args.scholar_id, args.max_pubs)
    
    if not publications:
        print("No publications fetched.")
        return
    
    # Find new publications
    new_entries = []
    for pub in publications:
        title = pub.get('bib', {}).get('title', '')
        if not title:
            continue
            
        if args.list_all:
            bibtex = pub_to_bibtex(pub)
            if bibtex:
                new_entries.append(bibtex)
        elif not is_duplicate(title, existing_titles):
            bibtex = pub_to_bibtex(pub)
            if bibtex:
                new_entries.append(bibtex)
                print(f"  NEW: {title[:60]}...")
    
    # Output results
    if args.list_all:
        print(f"\n{'='*60}")
        print(f"All {len(new_entries)} publications:")
        print('='*60)
    else:
        print(f"\n{'='*60}")
        print(f"Found {len(new_entries)} new publications (not in existing bib)")
        print('='*60)
    
    if not new_entries:
        print("No new entries to add.")
        return
    
    # Combine all entries
    combined = "\n".join(new_entries)
    
    if args.dry_run:
        print("\n--- DRY RUN: New entries ---\n")
        print(combined)
        print(f"\nTo save these entries, run: python {sys.argv[0]} --merge")
        
    elif args.merge:
        # Append to main bib file
        with open(BIB_FILE, 'a', encoding='utf-8') as f:
            f.write("\n\n% ===== New entries from Google Scholar =====\n")
            f.write(f"% Fetched on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(combined)
        print(f"\nAppended {len(new_entries)} entries to {BIB_FILE}")
        
    else:
        # Save to new file for review
        with open(NEW_BIB_FILE, 'w', encoding='utf-8') as f:
            f.write(f"% New entries from Google Scholar\n")
            f.write(f"% Fetched on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"% Author ID: {args.scholar_id}\n\n")
            f.write(combined)
        print(f"\nSaved {len(new_entries)} new entries to {NEW_BIB_FILE}")
        print("Review the file and run with --merge to append to papers.bib")


if __name__ == "__main__":
    main()
