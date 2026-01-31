from django.shortcuts import render, redirect
from products.models import Product
from categories.models import Category
from banners.models import Banner
from brands.models import Brand
from .models import CompanyInfo, HomePageContent, HomeFeature, NewsletterSubscriber
from django.contrib import messages

def home(request):
    banners = Banner.objects.filter(is_active=True).order_by('order')
    featured_categories = Category.objects.filter(is_featured=True, parent=None).order_by('order')[:4]
    featured_products = Product.objects.filter(is_featured=True, is_active=True).select_related('category', 'brand')[:8]
    brands = Brand.objects.filter(is_featured=True)
    
    # Get dynamic content
    company_info = CompanyInfo.objects.first()
    home_content = HomePageContent.objects.first()
    home_features = HomeFeature.objects.all()
    
    context = {
        'banners': banners,
        'featured_categories': featured_categories,
        'featured_products': featured_products,
        'brands': brands,
        'company_info': company_info,
        'home_content': home_content,
        'home_features': home_features,
    }
    return render(request, 'home.html', context)

def about(request):
    company_info = CompanyInfo.objects.first()
    return render(request, 'about.html', {'company_info': company_info})

def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            if NewsletterSubscriber.objects.filter(email=email).exists():
                messages.info(request, "You are already subscribed to our newsletter.")
            else:
                NewsletterSubscriber.objects.create(email=email)
                messages.success(request, "Thank you for subscribing to our newsletter!")
        else:
            messages.error(request, "Please provide a valid email address.")
            
    return redirect(request.META.get('HTTP_REFERER', 'home'))
