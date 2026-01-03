# frozen_string_literal: true

# Jekyll hook to run ensure_person_fields.py before the site builds
# This ensures all person profiles have required email and alias fields

Jekyll::Hooks.register :site, :after_init do |site|
  script_path = File.join(site.source, 'scripts', 'ensure_person_fields.py')
  
  if File.exist?(script_path)
    Jekyll.logger.info "Pre-build:", "Running ensure_person_fields.py..."
    
    result = system("python3 #{script_path}")
    
    if result
      Jekyll.logger.info "Pre-build:", "Person fields check completed"
    else
      Jekyll.logger.warn "Pre-build:", "ensure_person_fields.py returned non-zero exit code"
    end
  else
    Jekyll.logger.warn "Pre-build:", "ensure_person_fields.py not found at #{script_path}"
  end
end
