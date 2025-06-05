from weasyprint import HTML
import os

def convert_md_to_pdf(md_file_path, output_pdf_path):
    """
    Convert Markdown to PDF using WeasyPrint
    
    Args:
        md_file_path: Path to the Markdown file
        output_pdf_path: Path where the PDF will be saved
    """
    # Read the markdown content
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Create a simple HTML wrapper for the Markdown content
    # This is a basic approach - for better styling you might want to use a proper
    # Markdown to HTML converter first
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
            pre {{ background-color: #f5f5f5; padding: 10px; border-radius: 5px; overflow-x: auto; }}
            code {{ font-family: "Courier New", monospace; }}
            img {{ max-width: 100%; height: auto; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <pre>{md_content}</pre>
    </body>
    </html>
    """
    
    # Convert to PDF
    HTML(string=html_content).write_pdf(output_pdf_path)
    
    print(f"Converted {md_file_path} to {output_pdf_path}")
    return output_pdf_path