import os

file_path = r'd:\virjaproject\templates\base.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace any non-standard whitespace or zero-width characters that might break template tags
# \u200b is zero-width space, \u00a0 is non-breaking space
content = content.replace('\u200b', '').replace('\u00a0', ' ')

# Ensure the specific tag in the top bar is perfectly formed
# We'll replace the entire top bar section with a fresh, clean version
top_bar_pattern = r'<!-- Top Bar -->.*?<!-- Header & Navigation -->'
clean_top_bar = """<!-- Top Bar -->
    <div class="bg-gray-900 text-white py-2 border-b border-gray-800">
        <div class="container mx-auto px-4 flex justify-between items-center text-[11px] md:text-xs">
            <!-- Left: Email -->
            <div class="flex items-center gap-4">
                <a href="mailto:{{ company_info.email|default:'info@virjaautomation.com' }}"
                    class="flex items-center gap-2 hover:text-secondary transition text-white">
                    <i class="fas fa-envelope text-secondary"></i>
                    <span class="font-medium tracking-wide">{{ company_info.email|default:'info@virjaautomation.com' }}</span>
                </a>
            </div>

            <!-- Right: Social Media -->
            <div class="flex items-center gap-4">
                <div class="flex gap-3">
                    {% if company_info.facebook %}
                    <a href="{{ company_info.facebook }}" target="_blank" class="hover:text-secondary transition text-white"><i
                            class="fab fa-facebook-f"></i></a>
                    {% endif %}
                    {% if company_info.linkedin %}
                    <a href="{{ company_info.linkedin }}" target="_blank" class="hover:text-secondary transition text-white"><i
                            class="fab fa-linkedin-in"></i></a>
                    {% endif %}
                    {% if company_info.instagram %}
                    <a href="{{ company_info.instagram }}" target="_blank" class="hover:text-secondary transition text-white"><i
                            class="fab fa-instagram"></i></a>
                    {% endif %}
                    {% if company_info.twitter %}
                    <a href="{{ company_info.twitter }}" target="_blank" class="hover:text-secondary transition text-white"><i
                            class="fab fa-twitter"></i></a>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>

    <!-- Header & Navigation -->"""

import re
content = re.sub(top_bar_pattern, clean_top_bar, content, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Deep cleaned and fixed {file_path}")
