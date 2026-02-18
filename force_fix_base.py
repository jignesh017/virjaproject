import re
import os

file_path = r'd:\virjaproject\templates\base.html'

if not os.path.exists(file_path):
    print(f"File {file_path} not found")
    exit(1)

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to join {{ ... }} tags that are broken across lines
# Matches {{ followed by whitespace and newlines, then some content, and finally }}
# It replaces any internal newlines/excessive whitespace with a single space.
def join_tags(match):
    text = match.group(0)
    # Join the lines and replace multiple spaces with single space
    return ' '.join(text.split())

# Generic pattern for all {{ ... }} and {% ... %} tags
content = re.sub(r'({{.*?}}|{%.*?%})', join_tags, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Fixed {file_path}")
