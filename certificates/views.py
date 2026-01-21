from django.shortcuts import render
from .models import Certificate

def certificate_list(request):
    certificates = Certificate.objects.all().order_by('-created_at')
    return render(request, 'certificates/certificate_list.html', {'certificates': certificates})
