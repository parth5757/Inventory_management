import PyPDF2  # Make sure PyPDF2 is imported

# Assuming you're reading from a PDF file named 'your_file.pdf'
file_path = 'path_to_your_pdf_file.pdf'

# Open the PDF file in binary mode
with open('Think_Python.pdf', 'rb') as file:
    # Create a PdfReader object
    reader = PyPDF2.PdfReader(file)
    
    # Loop through each page in the PDF
    for page in reader.pages:
        # Extract text from the page
        text = page.extract_text()
        print(text)  # Print or process the text as needed
