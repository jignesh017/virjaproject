from django.shortcuts import render
from products.models import Product
from categories.models import Category
from banners.models import Banner
from brands.models import Brand
from .models import CompanyInfo

def home(request):
    banners = Banner.objects.filter(is_active=True).order_by('order')
    featured_categories = Category.objects.filter(is_featured=True, parent=None).order_by('order')[:4]
    featured_products = Product.objects.filter(is_featured=True, is_active=True).select_related('category', 'brand')[:8]
    brands = Brand.objects.filter(is_featured=True)
    
    context = {
        'banners': banners,
        'featured_categories': featured_categories,
        'featured_products': featured_products,
        'brands': brands,
    }
    return render(request, 'home.html', context)

def about(request):
    company_info = CompanyInfo.objects.first()
    return render(request, 'about.html', {'company_info': company_info})
