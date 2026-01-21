from django.shortcuts import render
from .models import Catalog

def catalog_list(request):
    catalogs = Catalog.objects.all().order_by('-created_at')
    return render(request, 'catalogs/catalog_list.html', {'catalogs': catalogs})
