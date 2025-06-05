import os
import sys
from simulate_pdf import simulate_pdf_conversion
from convert_using_llm import convert_to_markdown_using_llm

def main():
    # Define file paths
    readme_path = input("Enter the path to the README.md file: ")
    if not os.path.exists(readme_path):
        print(f"File {readme_path} does not exist!")
        sys.exit(1)
        
    # Define output directory
    output_dir = "output"
    temp_dir = "temp"
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)
    
    # Step 1: Read original README.md content
    print(f"\nStep 1: Reading original README.md content...")
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme_content = f.read()
    
    # Step 2: Simulate PDF conversion (create a text version that resembles PDF extraction)
    print(f"\nStep 2: Simulating PDF conversion and text extraction...")
    simulated_pdf_text = simulate_pdf_conversion(readme_path)
    simulated_pdf_path = os.path.join(temp_dir, os.path.basename(readme_path).replace(".md", "_simulated_pdf.txt"))
    
    # Step 3: Use LLM to convert README content to Markdown
    print(f"\nStep 3: Converting original README to Markdown using LLM...")
    readme_to_md = convert_to_markdown_using_llm(readme_content, "README")
    
    # Step 4: Use LLM to convert simulated PDF content to Markdown
    print(f"\nStep 4: Converting simulated PDF content to Markdown using LLM...")
    pdf_to_md = convert_to_markdown_using_llm(simulated_pdf_text, "PDF-like text")
    
    # Step 5: Save the results
    print(f"\nStep 5: Saving the results...")
    
    with open(os.path.join(output_dir, "readme_to_md.md"), 'w', encoding='utf-8') as f:
        f.write(readme_to_md)
        
    with open(os.path.join(output_dir, "simulated_pdf_to_md.md"), 'w', encoding='utf-8') as f:
        f.write(pdf_to_md)
    
    # Print summary
    print("\n=== Conversion Complete ===")
    print(f"Original README: {readme_path}")
    print(f"Simulated PDF text: {simulated_pdf_path}")
    print(f"README to Markdown: {os.path.join(output_dir, 'readme_to_md.md')}")
    print(f"Simulated PDF to Markdown: {os.path.join(output_dir, 'simulated_pdf_to_md.md')}")
    print("\nPlease compare these files to evaluate the quality of the conversion.")

if __name__ == "__main__":
    main()