require 'yaml'
require 'fileutils'

# Configuration
PEOPLE_DIR = '_people'
DATA_FILE = '_data/coauthors.yml'
COLLECTION_PERMALINK = '/people' # Base URL for the people collection

# Helper to generate first name variants
def generate_firstname_variants(firstname)
  variants = [firstname]
  # Add initials (e.g., "G." for "Gouri", "C. S." for "Chandra Sekhar")
  if firstname && firstname.length > 0
    parts = firstname.split(/\s+/)
    # Full initials: "C. S."
    full_initials = parts.map { |p| "#{p[0]}." }.join(" ")
    variants << full_initials
    
    # Compact initials: "C.S."
    compact_initials = parts.map { |p| "#{p[0]}." }.join("")
    variants << compact_initials if compact_initials != full_initials
    
    # First initial only: "C." (if different from full initials)
    first_initial = "#{parts[0][0]}."
    variants << first_initial if first_initial != full_initials
  end
  variants.uniq
end

# Helper to construct URL
def construct_url(relative_path)
  # Remove extension
  path_without_ext = relative_path.sub(/\.md$/, '')
  # Construct URL: /people/subdir/filename/
  "#{COLLECTION_PERMALINK}/#{path_without_ext}/"
end

coauthors = {}

# Iterate through all markdown files in _people
Dir.glob(File.join(PEOPLE_DIR, '**', '*.md')).each do |file_path|
  begin
    content = File.read(file_path)
    if content =~ /\A(---\s*\n.*?\n?)^((---|\.\.\.)\s*$\n?)/m
      front_matter = YAML.safe_load($1)
      
      lastname = front_matter['lastname']
      firstname = front_matter['firstname']
      
      next unless lastname && firstname

      key = lastname.downcase.strip
      
      # Generate variants
      firstname_variants = generate_firstname_variants(firstname)
      
      # Construct URL
      relative_path = file_path.sub("#{PEOPLE_DIR}/", '')
      url = construct_url(relative_path)
      
      # Create entry
      entry = {
        'firstname' => firstname_variants,
        'url' => url
      }

      # Initialize array for this lastname if not exists
      coauthors[key] ||= []
      
      # Check if this person is already added (avoid duplicates if any)
      unless coauthors[key].any? { |e| e['url'] == url }
        coauthors[key] << entry
      end
    end
  rescue => e
    puts "Error processing #{file_path}: #{e.message}"
  end
end

# Write to _data/coauthors.yml
File.open(DATA_FILE, 'w') do |file|
  file.write(coauthors.to_yaml)
end

puts "Successfully generated #{DATA_FILE} with #{coauthors.size} entries."
