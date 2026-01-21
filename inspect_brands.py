import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vproject.settings')
django.setup()

from brands.models import Brand
from categories.models import Category

brands = Brand.objects.all()
# for b in brands:
#     print(f"Brand ID: {b.id}, Name: '{b.name}'")

categories = Category.objects.all()
for c in categories:
    print(f"Cat ID: {c.id}, Name: '{c.name}'")

