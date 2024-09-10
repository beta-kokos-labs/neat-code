import re

def format_js(js_code):
    # Split the JavaScript code into tokens based on common separators
    tokens = re.split(r'(\s*[\{\}\(\)\;\,]\s*)', js_code)
    
    # Initialize variables
    formatted_code = []
    indent_level = 0
    indent_size = 4  # Number of spaces per indent level
    indent = ' ' * indent_size

    for token in tokens:
        stripped_token = token.strip()

        if stripped_token in ('{', '(', '['):
            formatted_code.append(indent * indent_level + stripped_token)
            indent_level += 1
        elif stripped_token in ('}', ')', ']'):
            indent_level -= 1
            formatted_code.append(indent * indent_level + stripped_token)
        elif stripped_token == ';':
            formatted_code.append(indent * indent_level + stripped_token)
        elif stripped_token:
            formatted_code.append(indent * indent_level + stripped_token)

    return '\n'.join(formatted_code)

def format_html(html_code):
    # Split HTML code into tags and text
    parts = re.split(r'(<[^>]+>)', html_code)
    formatted_code = []
    indent_level = 0
    indent_size = 4  # Number of spaces per indent level
    indent = ' ' * indent_size
    
    for part in parts:
        if part.startswith('<'):
            # Handle HTML tags
            if part.startswith('</'):
                indent_level -= 1
            formatted_code.append(indent * indent_level + part.strip())
            if not part.startswith('</') and not part.endswith('/>'):
                indent_level += 1
        else:
            # Handle text
            formatted_code.append(indent * indent_level + part.strip())

    return '\n'.join(formatted_code)

def format_code(code):
    # Separate HTML and JavaScript (assumes script tags for JS)
    html_part = re.split(r'(<script[^>]*>.*?</script>)', code, flags=re.DOTALL)
    formatted_html = []
    
    for part in html_part:
        if part.startswith('<script'):
            # Extract and format JavaScript inside <script> tags
            js_code = re.sub(r'</?script[^>]*>', '', part, flags=re.DOTALL)
            formatted_js = format_js(js_code)
            formatted_html.append(f'<script>\n{formatted_js}\n</script>')
        else:
            # Format HTML parts
            formatted_html.append(format_html(part))
    
    return ''.join(formatted_html)

# Example usage
source_code = """<!DOCTYPE html><html><head><title>Test</title></head><body><script>if(boolean){do_something(e);do_another_thing(e);and_then_one_more_thing(e)}</script></body></html>"""

formatted_code = format_code(source_code)
print(formatted_code)
