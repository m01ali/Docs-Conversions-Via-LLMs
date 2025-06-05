import pypdf

def extract_text_from_pdf(pdf_path):
    """
    Extract text content from a PDF file
    
    Args:
        pdf_path: Path to the PDF file
    
    Returns:
        String containing the extracted text
    """
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = pypdf.PdfReader(file)
            num_pages = len(reader.pages)
            
            for page_num in range(num_pages):
                page = reader.pages[page_num]
                text += page.extract_text() or ""
                text += "\n\n"  # Add spacing between pages
                
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return ""