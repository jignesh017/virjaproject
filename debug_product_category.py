import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vproject.settings')
django.setup()

from products.models import Product

def debug():
    try:
        p = Product.objects.get(slug='havells-industrial-cables-6-sqmm')
        print(f"Product: {p.name}")
        print(f"Category: {p.category.name!r}")
        print(f"Category Slug: {p.category.slug!r}")
        print(f"Category ID: {p.category.id}")
        
        # Check if name contains brackets
        if '{' in p.category.name:
            print("ALERT: Name contains curly braces!")
            
    except Product.DoesNotExist:
        print("Product not found")

if __name__ == '__main__':
    debug()
