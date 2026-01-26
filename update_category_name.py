import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vproject.settings')
django.setup()

from categories.models import Category

def update():
    try:
        c = Category.objects.get(slug='industrial-cables')
        print(f"Old Name: {c.name!r}")
        c.name = "TEST_CATEGORY"
        c.save()
        print(f"New Name: {c.name!r}")
    except Category.DoesNotExist:
        print("Category not found")

if __name__ == '__main__':
    update()
