import os
import re

def add_year_to_alumni_profiles(root_dir):
    alumni_dir = os.path.join(root_dir, '_people', 'alumni')
    
    for root, dirs, files in os.walk(alumni_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                
                # Extract year from path
                # Path structure: .../_people/alumni/<category>/<year>/<file.md>
                parts = file_path.split(os.sep)
                try:
                    # Assuming the year is the immediate parent folder
                    year_str = parts[-2]
                    if not year_str.isdigit() or len(year_str) != 4:
                        print(f"Skipping {file_path}: Parent folder '{year_str}' is not a year.")
                        continue
                    
                    year = int(year_str)
                    
                    with open(file_path, 'r') as f:
                        content = f.read()
                    
                    # Check if year already exists
                    if re.search(r'^year:\s*\d+', content, re.MULTILINE):
                        print(f"Skipping {file_path}: Year already exists.")
                        continue
                    
                    # Add year to front matter
                    # Assuming front matter ends with ---
                    if content.startswith('---'):
                        # Find the second ---
                        second_dash_index = content.find('\n---', 3)
                        if second_dash_index != -1:
                            new_content = content[:second_dash_index] + f'\nyear: {year}' + content[second_dash_index:]
                            
                            with open(file_path, 'w') as f:
                                f.write(new_content)
                            print(f"Updated {file_path} with year {year}")
                        else:
                            print(f"Skipping {file_path}: Could not find end of front matter.")
                    else:
                        print(f"Skipping {file_path}: No front matter found.")
                        
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    add_year_to_alumni_profiles('/Users/gourishanker/spectrum-lab-iisc.github.io')
