import os
import django
import random

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vproject.settings')
django.setup()

from categories.models import Category
from brands.models import Brand
from products.models import Product

def populate():
    print("Populating data with images...")

    # --- Brands ---
    brands_list = [
        "Polycab", "L&T (Lauritz Knudsen)", "Siemens", "Schneider Electric", 
        "ABB", "Havells", "Legrand", "Finolex"
    ]
    brands_objs = []
    print("Creating Brands...")
    for b_name in brands_list:
        brand, created = Brand.objects.get_or_create(
            name=b_name, 
            defaults={'is_featured': True, 'logo': 'brands/placeholder.png'}
        )
        # Update logo if it exists but has no logo (or just force it for this demo)
        if not brand.logo:
            brand.logo = 'brands/placeholder.png'
            brand.save()
        brands_objs.append(brand)

    # --- Categories ---
    # Map Category Names to Images we generated
    cat_images = {
        "Switchgears": "categories/switchgear.png",
        "Wires & Cables": "categories/cables.png",
        "Automation": "categories/automation.png",
        # Use fallback for others
        "Lighting": "categories/switchgear.png", 
        "Motors": "categories/automation.png"
    }

    categories_data = {
        "Switchgears": ["MCB", "MCCB", "ACB", "Distribution Boards", "Contactors"],
        "Wires & Cables": ["Industrial Cables", "Building Wires", "Communication Cables", "Control Cables"],
        "Automation": ["PLCs", "HMI", "VFDs", "Sensors", "Relays"],
        "Lighting": ["Industrial High Bay", "Street Lights", "Panel Lights", "Flood Lights"],
        "Motors": ["Induction Motors", "Servo Motors", "Stepper Motors"]
    }

    categories_objs = {}
    print("Creating Categories...")
    for parent_name, children in categories_data.items():
        img_path = cat_images.get(parent_name, "categories/switchgear.png")
        parent, _ = Category.objects.get_or_create(
            name=parent_name,
            defaults={'is_featured': True, 'image': img_path}
        )
        if hasattr(parent, 'image') and not parent.image:
             parent.image = img_path
             parent.save()

        categories_objs[parent_name] = {"obj": parent, "children": []}
        
        for child_name in children:
            child, _ = Category.objects.get_or_create(name=child_name, parent=parent)
            categories_objs[parent_name]["children"].append(child)

    # --- Products ---
    print("Creating Products...")
    
    # Switchgear Products
    sg_cat = categories_objs["Switchgears"]["children"]
    for i in range(12):
        cat = random.choice(sg_cat)
        brand = random.choice(brands_objs)
        name = f"{brand.name} {cat.name} {random.randint(10, 800)}A"
        Product.objects.get_or_create(
            name=name,
            defaults={
                'category': cat,
                'brand': brand,
                'description': f"High quality {cat.name} from {brand.name}. Suitable for industrial applications. Rated for {random.randint(230, 415)}V.",
                'specification': f"Rated Current: {random.randint(10, 800)}A\nBreaking Capacity: {random.randint(10, 50)}kA\nPoles: {random.choice(['1P', '2P', '3P', '4P'])}",
                'is_featured': random.choice([True, False]),
                'main_image': 'products/mcb.png'
            }
        )

    # Cable Products
    cable_cat = categories_objs["Wires & Cables"]["children"]
    for i in range(12):
        cat = random.choice(cable_cat)
        brand = random.choice(brands_objs)
        name = f"{brand.name} {cat.name} {random.choice(['2.5', '4', '6', '10', '16'])} sq.mm"
        Product.objects.get_or_create(
            name=name,
            defaults={
                'category': cat,
                'brand': brand,
                'description': f"Premium grade {cat.name} by {brand.name}. Multistrand copper conductor, PVC insulated.",
                'specification': f"Size: {random.choice(['2.5', '4', '6', '10'])} sq.mm\nCores: {random.randint(1, 4)}\nVoltage Grade: 1100V",
                'is_featured': random.choice([True, False]),
                'main_image': 'categories/cables.png' # Reusing category image if product image not unique
            }
        )

    # Automation Products
    auto_cat = categories_objs["Automation"]["children"]
    for i in range(10):
        cat = random.choice(auto_cat)
        brand = random.choice(brands_objs)
        name = f"{brand.name} {cat.name} Series-{random.choice(['X', 'Y', 'Z'])}{random.randint(100, 999)}"
        Product.objects.get_or_create(
            name=name,
            defaults={
                'category': cat,
                'brand': brand,
                'description': f"Advanced {cat.name} solution for industrial automation. High reliability and performance.",
                'specification': f"Input: 24V DC\nOutput: Relay/Transistor\nCommunication: Modbus/Ethernet",
                'is_featured': True,
                'main_image': 'categories/automation.png'
            }
        )

    print("Data population with images complete!")

if __name__ == '__main__':
    populate()
