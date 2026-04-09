from django.shortcuts import render
from .models import PriceList

def pricelist_list(request):
    pricelists = PriceList.objects.all().order_by('-created_at')
    return render(request, 'pricelists/pricelist_list.html', {'pricelists': pricelists})
