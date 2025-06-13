## Documents To Markdown Via LLMs
A tool for converting various document formats to Markdown using Large Language Models, built on top of Microsoft's MarkItDown utility.

### Project Overview
This project provides tools for converting different document formats (PDFs, HTML, etc.) to Markdown format, making them more accessible for Large Language Models and text analysis pipelines. It includes:

1. A simple Python converter `doc_to_markdown.py` for basic document conversion
2. A GUI interface `gui.py` for easier interaction
3. Integration with Microsoft's [MarkItDown](https://github.com/microsoft/markitdown) library for more robust conversions

### Directory Structure
- **Root**: Contains the main Python scripts and configuration files
- **markdown_output/**: Stores converted Markdown documents and associated images
- **markitdown/**: Submodule containing Microsoft's MarkItDown utility
### Installation
1. Clone this repository:

`
git clone https://github.com/yourusername/Docs-to-md-via-LLMs.git
cd Docs-to-md-via-LLMs
`

2. Install required dependencies:

`pip install -r requirements.txt`

3. Install MarkItDown with all optional dependencies:

`pip install 'markitdown[all]'`

 or you may clone the official repo
### Usage
**Basic Document Conversion:**

`python doc_to_markdown.py path/to/your/document.pdf`


### Supported File Types
- PDF documents
- HTML pages
- Word documents
- Excel spreadsheets 

#### License
This project is licensed under the MIT License 

#### Acknowledgments
- This project uses MarkItDown from Microsoft's AutoGen team
- Special thanks to all contributors who have helped shape this project