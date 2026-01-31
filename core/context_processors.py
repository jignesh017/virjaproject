from categories.models import Category
from .models import CompanyInfo, HomePageContent, HomeFeature

def site_settings(request):
    """
    Returns global site settings and home page content.
    """
    return {
        'company_info': CompanyInfo.objects.first(),
        'home_content': HomePageContent.objects.first(),
        'home_features': HomeFeature.objects.all(),
    }

def global_categories(request):
    """
    Returns top-level categories with their children pre-fetched for the mega menu.
    """
    categories = Category.objects.filter(parent=None).prefetch_related('children__children').order_by('order', 'name')
    return {
        'mega_menu_categories': categories
    }
