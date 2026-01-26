import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vproject.settings')
django.setup()

from categories.models import Category
from brands.models import Brand
from products.models import Product

print("--- Check Categories ---")
for c in Category.objects.all()[:10]:
    print(f"ID: {c.id}, Name: {c.name!r}, Slug: {c.slug}")

print("\n--- Check Brands ---")
for b in Brand.objects.all()[:10]:
    print(f"ID: {b.id}, Name: {b.name!r}, Slug: {b.slug}")

print("\n--- Check Products ---")
for p in Product.objects.all()[:5]:
    print(f"ID: {p.id}, Name: {p.name!r}, Slug: {p.slug}, Brand: {p.brand.name if p.brand else 'None'}")
