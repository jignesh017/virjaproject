from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product
from categories.models import Category
from brands.models import Brand

def product_list(request):
    products = Product.objects.filter(is_active=True).order_by('-created_at')
    
    # Filters
    category_slug = request.GET.get('category')
    brand_slug = request.GET.get('brand')
    query = request.GET.get('q')
    
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        # Include children products
        categories = [selected_category] + list(selected_category.children.all())
        products = products.filter(category__in=categories)

    if brand_slug:
        products = products.filter(brand__slug=brand_slug)
        
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    # Pagination
    paginator = Paginator(products, 12) # 12 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': Category.objects.filter(parent=None),
        'brands': Brand.objects.all(),
        'selected_category': selected_category,
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(category=product.category, is_active=True).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)
