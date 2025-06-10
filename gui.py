import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
from doc_to_markdown import DocumentConverter

class MarkdownConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Document to Markdown Converter")
        self.root.geometry("600x400")
        
        # Configure styles
        self.root.configure(bg="#f0f0f0")
        
        # Variables
        self.input_file = tk.StringVar()
        self.api_key = tk.StringVar()
        self.site_url = tk.StringVar(value="https://example.com")
        self.site_name = tk.StringVar(value="Document Converter")
        self.status = tk.StringVar(value="Ready")
        
        # Create main frame
        main_frame = tk.Frame(self.root, padx=20, pady=20, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create form elements
        self._create_form_elements(main_frame)
        
    def _create_form_elements(self, parent):
        # File selection
        file_frame = tk.Frame(parent, bg="#f0f0f0")
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(file_frame, text="Input File:", bg="#f0f0f0").pack(side=tk.LEFT)
        tk.Entry(file_frame, textvariable=self.input_file, width=40).pack(side=tk.LEFT, padx=(5, 5))
        tk.Button(file_frame, text="Browse", command=self._browse_file).pack(side=tk.LEFT)
        
        # API Key
        api_frame = tk.Frame(parent, bg="#f0f0f0")
        api_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(api_frame, text="OpenRouter API Key:", bg="#f0f0f0").pack(side=tk.LEFT)
        tk.Entry(api_frame, textvariable=self.api_key, width=40, show="*").pack(side=tk.LEFT, padx=(5, 5))
        
        # Site URL
        url_frame = tk.Frame(parent, bg="#f0f0f0")
        url_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(url_frame, text="Site URL:", bg="#f0f0f0").pack(side=tk.LEFT)
        tk.Entry(url_frame, textvariable=self.site_url, width=40).pack(side=tk.LEFT, padx=(5, 5))
        
        # Site Name
        name_frame = tk.Frame(parent, bg="#f0f0f0")
        name_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(name_frame, text="Site Name:", bg="#f0f0f0").pack(side=tk.LEFT)
        tk.Entry(name_frame, textvariable=self.site_name, width=40).pack(side=tk.LEFT, padx=(5, 5))
        
        # Convert button
        btn_frame = tk.Frame(parent, bg="#f0f0f0")
        btn_frame.pack(fill=tk.X, pady=(10, 10))
        
        tk.Button(
            btn_frame, 
            text="Convert to Markdown", 
            command=self._start_conversion,
            bg="#4CAF50", 
            fg="white", 
            font=("Arial", 12, "bold"),
            padx=10,
            pady=5
        ).pack()
        
        # Status
        status_frame = tk.Frame(parent, bg="#f0f0f0")
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(status_frame, text="Status:", bg="#f0f0f0").pack(side=tk.LEFT)
        tk.Label(status_frame, textvariable=self.status, bg="#f0f0f0", fg="#333").pack(side=tk.LEFT, padx=(5, 0))
    
    def _browse_file(self):
        filetypes = (
            ("All supported files", "*.pdf;*.docx;*.doc;*.xlsx;*.xls;*.html;*.htm;*.md;*.txt"),
            ("PDF files", "*.pdf"),
            ("Word documents", "*.docx;*.doc"),
            ("Excel spreadsheets", "*.xlsx;*.xls"),
            ("HTML files", "*.html;*.htm"),
            ("Markdown files", "*.md"),
            ("Text files", "*.txt"),
            ("All files", "*.*")
        )
        
        filename = filedialog.askopenfilename(
            title="Select a document to convert",
            filetypes=filetypes
        )
        
        if filename:
            self.input_file.set(filename)
    
    def _start_conversion(self):
        input_file = self.input_file.get()
        api_key = self.api_key.get()
        site_url = self.site_url.get()
        site_name = self.site_name.get()
        
        if not input_file:
            messagebox.showerror("Error", "Please select an input file")
            return
        
        if not os.path.exists(input_file):
            messagebox.showerror("Error", "Input file does not exist")
            return
        
        if not api_key:
            messagebox.showerror("Error", "Please enter your OpenRouter API key")
            return
        
        # Start conversion in a separate thread
        self.status.set("Converting...")
        thread = threading.Thread(
            target=self._run_conversion,
            args=(input_file, api_key, site_url, site_name)
        )
        thread.daemon = True
        thread.start()
    
    def _run_conversion(self, input_file, api_key, site_url, site_name):
        try:
            converter = DocumentConverter(
                openrouter_api_key=api_key,
                site_url=site_url,
                site_name=site_name
            )
            
            output_path = converter.convert_file(input_file)
            
            # Update UI from the main thread
            self.root.after(0, lambda: self._show_success(output_path))
            
        except Exception as e:
            # Update UI from the main thread
            self.root.after(0, lambda: self._show_error(str(e)))
    
    def _show_success(self, output_path):
        self.status.set("Conversion completed")
        messagebox.showinfo(
            "Conversion Successful", 
            f"Document successfully converted to:\n{output_path}"
        )
    
    def _show_error(self, error_message):
        self.status.set("Conversion failed")
        messagebox.showerror("Error", f"Conversion failed: {error_message}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MarkdownConverterGUI(root)
    root.mainloop()