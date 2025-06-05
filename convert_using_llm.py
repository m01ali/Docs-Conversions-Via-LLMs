from openai import OpenAI
from config import OPENROUTER_API_KEY, REFERER_URL, SITE_NAME
import os

# Initialize OpenAI client with OpenRouter settings
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

def convert_to_markdown_using_llm(text, input_type, model="openai/gpt-4o", max_tokens=4096):
    """
    Convert text content to well-formatted Markdown using an LLM
    
    Args:
        text: The text content to convert
        input_type: Description of the input (e.g. "PDF", "README")
        model: The model to use
        max_tokens: Maximum tokens for the response
        
    Returns:
        Markdown-formatted text
    """
    print(f"Converting {input_type} to Markdown using {model}...")
    
    # Prepare the prompt based on input type
    prompt = f"""
    Convert the following {input_type} content into clean, well-formatted Markdown.
    
    Pay special attention to:
    1. Preserve all headings with proper hierarchy (# for h1, ## for h2, etc.)
    2. Maintain all lists (ordered and unordered)
    3. Preserve code blocks with the correct language syntax highlighting
    4. Convert tables to Markdown table format
    5. Include image references with proper alt text
    6. Maintain links with correct syntax
    7. Preserve the overall structure and organization of the content
    
    Here's the content to convert:
    
    {text}
    """
    
    try:
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": REFERER_URL,
                "X-Title": SITE_NAME,
            },
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=max_tokens
        )
        
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error using LLM for conversion: {e}")
        return ""