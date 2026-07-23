from django.shortcuts import render
from brands.models import Brand

def pricelist_list(request):
    brands = (
        Brand.objects
        .prefetch_related('pricelists')
        .filter(pricelists__isnull=False)
        .distinct()
    )

    return render(
        request,
        'pricelists/pricelist_list.html',
        {
            'brands': brands
        }
    )