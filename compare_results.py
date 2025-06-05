import os
import difflib
import re

def count_markdown_elements(content):
    """Count various Markdown elements in the content"""
    results = {
        "headings": len(re.findall(r'^#{1,6}\s+.+$', content, re.MULTILINE)),
        "code_blocks": len(re.findall(r'```\w*\n[\s\S]*?\n```', content)),
        "links": len(re.findall(r'\[.+?\]\(.+?\)', content)),
        "images": len(re.findall(r'!\[.+?\]\(.+?\)', content)),
        "tables": len(re.findall(r'\|.+\|[\r\n]\|[-:]+\|', content)),
        "lists": len(re.findall(r'^\s*[-*+]\s+.+$', content, re.MULTILINE)) + 
                 len(re.findall(r'^\s*\d+\.\s+.+$', content, re.MULTILINE)),
    }
    return results

def compare_markdown_files(file1_path, file2_path, original_path=None):
    """Compare two Markdown files and provide statistics"""
    with open(file1_path, 'r', encoding='utf-8') as f:
        file1_content = f.read()
        
    with open(file2_path, 'r', encoding='utf-8') as f:
        file2_content = f.read()
        
    original_content = None
    if original_path:
        with open(original_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
    
    # Count elements in each file
    file1_elements = count_markdown_elements(file1_content)
    file2_elements = count_markdown_elements(file2_content)
    original_elements = count_markdown_elements(original_content) if original_content else None
    
    # Calculate similarity score
    similarity = difflib.SequenceMatcher(None, file1_content, file2_content).ratio()
    
    # Print comparison
    print("\n=== Markdown Comparison Results ===")
    print(f"File 1: {os.path.basename(file1_path)}")
    print(f"File 2: {os.path.basename(file2_path)}")
    print(f"\nSimilarity Score: {similarity:.2%}")
    
    print("\nMarkdown Elements Comparison:")
    print(f"{'Element':<15} {'File 1':<10} {'File 2':<10} {'Original':<10}")
    print("-" * 50)
    
    for element in file1_elements:
        file1_val = file1_elements[element]
        file2_val = file2_elements[element]
        original_val = original_elements[element] if original_elements else "N/A"
        print(f"{element:<15} {file1_val:<10} {file2_val:<10} {original_val:<10}")
    
    # Provide insights
    print("\n=== Insights ===")
    if similarity > 0.9:
        print("The two conversions are very similar.")
    elif similarity > 0.7:
        print("The conversions have significant similarities but also notable differences.")
    else:
        print("The conversions differ substantially.")
    
    # Compare with original if available
    if original_elements:
        print("\nPreservation of Original Elements:")
        for element in original_elements:
            original_val = original_elements[element]
            file1_val = file1_elements[element]
            file2_val = file2_elements[element]
            
            file1_preservation = (file1_val / original_val * 100) if original_val > 0 else 0
            file2_preservation = (file2_val / original_val * 100) if original_val > 0 else 0
            
            print(f"{element:<15} Original: {original_val}, File 1: {file1_preservation:.1f}%, File 2: {file2_preservation:.1f}%")

def main():
    readme_to_md = os.path.join("output", "readme_to_md.md")
    pdf_to_md = os.path.join("output", "simulated_pdf_to_md.md")
    original_readme = input("Enter the path to the original README.md file for comparison (or press Enter to skip): ")
    
    if not os.path.exists(readme_to_md) or not os.path.exists(pdf_to_md):
        print("Error: Output files not found. Run the conversion first.")
        return
        
    if original_readme and not os.path.exists(original_readme):
        print(f"Warning: Original README file {original_readme} not found. Proceeding without original comparison.")
        original_readme = None
        
    compare_markdown_files(readme_to_md, pdf_to_md, original_readme if original_readme else None)

if __name__ == "__main__":
    main()