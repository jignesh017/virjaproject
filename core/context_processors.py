from categories.models import Category

def global_categories(request):
    """
    Returns top-level categories with their children pre-fetched for the mega menu.
    """
    categories = Category.objects.filter(parent=None).prefetch_related('children__children').order_by('order', 'name')
    return {
        'mega_menu_categories': categories
    }
