require 'pdf-reader'

reader = PDF::Reader.new("CSSCV.pdf")

File.open("csscv.txt", "w") do |file|
  reader.pages.each do |page|
    file.write(page.text)
    file.write("\n")
  end
end

puts "Successfully extracted text to csscv.txt"
