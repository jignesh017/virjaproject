from django.shortcuts import render
from .models import Brand

def brand_list(request):
    brands = Brand.objects.all()
    return render(request, 'brands/brand_list.html', {'brands': brands})
