
import os
import django
import sys

# Add project root to path
sys.path.append(r'c:\Users\BHUT\Desktop\virja project')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vproject.settings')
django.setup()

from categories.models import Category

print("--- Checking Categories ---")
categories = Category.objects.filter(parent=None).prefetch_related('children')
for cat in categories:
    print(f"Parent: '{cat.name}' (Slug: {cat.slug})")
    for child in cat.children.all():
        print(f"  - Child: '{child.name}' (Slug: {child.slug})")
