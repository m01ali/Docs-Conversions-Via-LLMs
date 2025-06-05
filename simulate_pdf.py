def simulate_pdf_conversion(md_file_path):
    """
    Simulate the effect of converting Markdown to PDF and then back to text
    by stripping some formatting and structure that might be lost in PDF conversion.
    
    Args:
        md_file_path: Path to the Markdown file
        
    Returns:
        String containing the simplified text (simulating PDF extraction)
    """
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Simulate some of the formatting losses that happen in PDF conversion
    
    # Replace code blocks with simplified versions (lose syntax highlighting)
    import re
    md_content = re.sub(r'```(\w+)\n', '```\n', md_content)
    
    # Simplify table formatting (tables often lose structure in PDF extraction)
    lines = md_content.split('\n')
    simplified_lines = []
    in_table = False
    
    for line in lines:
        if line.startswith('|') and '-' in line and '|' in line[1:]:
            # This is likely a table header separator, skip it
            in_table = True
            continue
        elif line.startswith('|') and in_table:
            # Convert table row to plain text with spaces
            cleaned = line.replace('|', ' ').strip()
            simplified_lines.append(cleaned)
        else:
            in_table = False
            simplified_lines.append(line)
    
    # Join lines back together
    simulated_text = '\n'.join(simplified_lines)
    
    # Create the simulated PDF text file
    output_path = md_file_path.replace('.md', '_simulated_pdf.txt')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(simulated_text)
    
    print(f"Created simulated PDF text extraction at {output_path}")
    return simulated_text