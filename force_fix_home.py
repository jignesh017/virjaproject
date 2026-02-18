import re
import os

file_path = r'd:\virjaproject\templates\home.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define patterns to fix
# Pattern 1: Join split {{ ... }} tags that are broken across lines
# limiting to specific known tags to be safe
patterns = [
    (r'{{\s*\n\s*home_content\.hero_fallback_title', r'{{ home_content.hero_fallback_title'),
    (r'{{\s*\n\s*home_content\.hero_fallback_text', r'{{ home_content.hero_fallback_text'),
    (r'{{\s*\n\s*home_content\.categories_subtitle', r'{{ home_content.categories_subtitle'),
    (r'{{\s*\n\s*home_content\.categories_title', r'{{ home_content.categories_title'),
    (r'{{\s*\n\s*home_content\.featured_products_subtitle', r'{{ home_content.featured_products_subtitle'),
    (r'{{\s*\n\s*home_content\.featured_products_title', r'{{ home_content.featured_products_title'),
    (r'{{\s*\n\s*home_content\.brands_title', r'{{ home_content.brands_title'),
    (r'{{\s*\n\s*home_content\.cta_title', r'{{ home_content.cta_title'),
    (r'{{\s*\n\s*home_content\.cta_text', r'{{ home_content.cta_text'),
]

# Specifically handle the multi-line split where }} is on a new line
# Example: {{ ... \n ... }} -> {{ ... ... }}
# We need to capture the content between {{ and }} and remove newlines
def join_tags(match):
    text = match.group(0)
    return text.replace('\n', ' ').replace('\r', '').replace('  ', ' ')

# More generic approach for the specific tags we care about
# Match {{ [whitespace] home_content.X [anything] }} including newlines
tag_names = [
    'hero_fallback_title',
    'hero_fallback_text',
    'categories_subtitle',
    'categories_title',
    'featured_products_subtitle',
    'featured_products_title',
    'brands_title',
    'cta_title',
    'cta_text'
]

for tag in tag_names:
    # Regex to find the tag spanning multiple lines
    # {{ \s* home_content.tag \s* |default:.... \s* }}
    # We use a broad match for the content defaults
    pattern = re.compile(r'{{\s*home_content\.' + tag + r'[^}]+}}', re.DOTALL)
    
    def replacement(m):
        return ' '.join(m.group(0).split())
        
    content = pattern.sub(replacement, content)

# Check specifically for the ones that might have strictly matched the previous broken format
# Ensure no double indentation or weird spaces remains if possible, but mainly join lines.

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Fixed {file_path}")
