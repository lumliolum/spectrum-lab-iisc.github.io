import sys

try:
    from pypdf import PdfReader
except ImportError:
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        print("Error: pypdf or PyPDF2 not installed.")
        sys.exit(1)

try:
    reader = PdfReader("CSSCV.pdf")
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    
    with open("csscv.txt", "w") as f:
        f.write(text)
    print("Successfully extracted text to csscv.txt")
except Exception as e:
    print(f"Error extracting text: {e}")
    sys.exit(1)
