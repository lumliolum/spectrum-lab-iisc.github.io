import os
import glob
from ruamel.yaml import YAML

# Initialize YAML handler
yaml = YAML()
yaml.preserve_quotes = True
yaml.indent(mapping=2, sequence=4, offset=2)

CONFIG_PATH = 'admin/config.yml'
PEOPLE_DIR = '_people'

def get_all_fields_from_markdown(folder_path):
    """Scans all markdown files in a folder and returns a set of all keys found in front matter."""
    fields = set()
    # Handle both flat and nested structures (e.g., _people/alumni/phd-graduates/2018/name.md)
    search_path = os.path.join(folder_path, '**/*.md')
    files = glob.glob(search_path, recursive=True)
    
    for file_path in files:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                # Extract front matter
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        front_matter = yaml.load(parts[1])
                        if front_matter:
                            fields.update(front_matter.keys())
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            
    return fields

def sync_config():
    """Updates admin/config.yml with missing fields from people collections."""
    print(f"Loading {CONFIG_PATH}...")
    with open(CONFIG_PATH, 'r') as f:
        config = yaml.load(f)

    updated = False
    
    # Iterate through collections
    for collection in config.get('collections', []):
        # Check if it's a people or alumni collection
        # We can identify them by the folder path starting with _people
        folder = collection.get('folder')
        if folder and folder.startswith(PEOPLE_DIR):
            print(f"Processing collection: {collection['name']} ({folder})")
            
            # Get existing fields in config
            existing_fields = {field['name'] for field in collection.get('fields', [])}
            
            # Get actual fields from markdown files
            actual_fields = get_all_fields_from_markdown(folder)
            
            # Identify missing fields
            missing_fields = actual_fields - existing_fields
            
            # Exclude 'layout' and 'alias' as requested/standard
            missing_fields.discard('layout')
            missing_fields.discard('alias')
            
            if missing_fields:
                print(f"  Found missing fields: {missing_fields}")
                for field_name in missing_fields:
                    # Determine widget type (simple heuristic, default to string)
                    # In a more advanced version, we could analyze values to guess type
                    new_field = {
                        'label': field_name.replace('_', ' ').title(),
                        'name': field_name,
                        'widget': 'string',
                        'required': False
                    }
                    
                    # Add to collection fields
                    collection['fields'].append(new_field)
                    updated = True
                    print(f"  Added field: {field_name}")
            else:
                print("  No missing fields.")

    if updated:
        print(f"Saving updates to {CONFIG_PATH}...")
        with open(CONFIG_PATH, 'w') as f:
            yaml.dump(config, f)
        print("Done.")
    else:
        print("No changes needed.")

if __name__ == "__main__":
    sync_config()
