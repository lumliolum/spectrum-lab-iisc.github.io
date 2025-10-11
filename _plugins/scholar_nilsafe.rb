# Monkey patch to make jekyll-scholar resilient when a query yields nil
# This prevents "private method `select` called for nil" errors when
# bibliography[query] returns nil (e.g., malformed/empty query)

module Jekyll
  class Scholar
    module Utilities
      def entries
        # Resolve the query (from tag or config)
        q = query || config['query']

        # Attempt to run the query against the bibliography
        result = begin
          bibliography[q]
        rescue StandardError
          nil
        end

        # Fallbacks when result is nil or does not act like a collection
        collection =
          if result.respond_to?(:select)
            result
          elsif bibliography.respond_to?(:to_a)
            bibliography.to_a
          else
            []
          end

        # Keep only real BibTeX::Entry items, then sort with existing logic
        sort collection.select { |x| x.instance_of?(BibTeX::Entry) }
      end
    end
  end
end
