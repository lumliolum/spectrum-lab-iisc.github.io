require 'nokogiri'

module Jekyll
  module LinkCoauthorsFilter
    def link_coauthors(input)
      return input if input.nil? || input.empty?

      site = @context.registers[:site]
      coauthors = site.data['coauthors']
      return input unless coauthors

      # Build a mapping of "lowercase full name" -> url
      # and a list of names to match
      # We use a cache to avoid rebuilding this for every page if possible, 
      # but Liquid filters are instantiated per render. 
      # We can store it in site.config to cache it across calls.
      
      unless site.config['coauthors_map']
        name_map = {}
        
        coauthors.each do |lastname_key, people|
          # people is a list of entries
          people.each do |person|
            url = person['url']
            firstnames = person['firstname']
            
            firstnames.each do |fname|
              # Construct full name pattern: "Firstname Lastname"
              # lastname_key is already lowercase from the YAML key
              # fname might have capitalization
              
              full_name_str = "#{fname} #{lastname_key}".downcase.strip
              
              # Store in map
              # We might have collisions if two people have exact same name,
              # but the coauthors.yml structure groups by lastname.
              # If same lastname and same firstname variant, it's ambiguous.
              # We'll just take the last one or ignore.
              name_map[full_name_str] = url
            end
          end
        end
        
        # Sort names by length (descending) to match longest first
        sorted_names = name_map.keys.sort_by { |n| -n.length }
        
        site.config['coauthors_map'] = name_map
        site.config['coauthors_sorted_names'] = sorted_names
      end

      name_map = site.config['coauthors_map']
      sorted_names = site.config['coauthors_sorted_names']
      
      return input if sorted_names.empty?

      # Create a regex from the sorted names
      # Escape special characters in names
      # Use \b boundaries, but handle cases where name ends/starts with non-word char (like ".")
      # Actually, \b matches between \w and \W. 
      # "J." ends with ".", which is \W. So "J." followed by space is "J.\s".
      # "J." is "\w\W". \b matches after J. 
      # Let's just use simple escaping and look for word boundaries or whitespace.
      # A robust pattern: (?<!\w)name(?!\w) might be better than \b if names contain punctuation.
      
      # Optimization: Join with |
      pattern_str = sorted_names.map { |n| Regexp.escape(n) }.join('|')
      regex = /(?<!\w)(#{pattern_str})(?!\w)/i

      # Parse HTML fragment
      doc = Nokogiri::HTML.fragment(input)

      # Traverse text nodes
      doc.traverse do |node|
        if node.text? && node.parent.name != 'a' && node.parent.name != 'script' && node.parent.name != 'style' && node.parent.name != 'pre' && node.parent.name != 'code'
          content = node.content
          
          # Check if any name exists in content
          if content.match?(regex)
            new_content = content.gsub(regex) do |match|
              match_lower = match.downcase
              url = name_map[match_lower]
              
              if url
                "<a href=\"#{url}\" class=\"coauthor-link\">#{match}</a>"
              else
                match # Should not happen if regex matches
              end
            end
            
            # Replace node with new HTML
            # We need to parse the new content as HTML fragment because it contains <a> tags
            node.replace(Nokogiri::HTML.fragment(new_content))
          end
        end
      end

      doc.to_html
    end
  end
end

Liquid::Template.register_filter(Jekyll::LinkCoauthorsFilter)
