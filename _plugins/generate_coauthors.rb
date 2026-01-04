# frozen_string_literal: true
require 'yaml'

# Jekyll hook to generate coauthors.yml from _people files
# This ensures the coauthors data is always up-to-date with the people profiles

Jekyll::Hooks.register :site, :after_init do |site|
  Jekyll.logger.info "Coauthors:", "Generating coauthors data..."
  
  people_dir = File.join(site.source, '_people')
  data_file = File.join(site.source, '_data', 'coauthors.yml')
  collection_permalink = '/people' # Base URL for the people collection

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
  def construct_url(relative_path, collection_permalink)
    # Remove extension
    path_without_ext = relative_path.sub(/\.md$/, '')
    # Construct URL: /people/subdir/filename/
    "#{collection_permalink}/#{path_without_ext}/"
  end

  coauthors = {}
  
  if Dir.exist?(people_dir)
    Dir.glob(File.join(people_dir, '**', '*.md')).each do |file_path|
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
          relative_path = file_path.sub("#{people_dir}/", '')
          url = construct_url(relative_path, collection_permalink)
          
          # Create entry
          entry = {
            'firstname' => firstname_variants,
            'url' => url
          }

          # Initialize array for this lastname if not exists
          coauthors[key] ||= []
          
          # Check if this person is already added (avoid duplicates)
          unless coauthors[key].any? { |e| e['url'] == url }
            coauthors[key] << entry
          end
        end
      rescue => e
        Jekyll.logger.warn "Coauthors:", "Error processing #{file_path}: #{e.message}"
      end
    end

    # Write to _data/coauthors.yml
    File.open(data_file, 'w') do |file|
      file.write(coauthors.to_yaml)
    end
    
    Jekyll.logger.info "Coauthors:", "Generated #{coauthors.size} entries in #{data_file}"
  else
    Jekyll.logger.warn "Coauthors:", "_people directory not found at #{people_dir}"
  end
end
