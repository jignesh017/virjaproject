from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Enquiry
from core.models import CompanyInfo

def contact(request):
    company_info = CompanyInfo.objects.first()
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Save to DB
        Enquiry.objects.create(name=name, email=email, phone=phone, message=message)

        # Send Email
        subject = f"New Business Enquiry from {name}"
        msg_body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message}"
        try:
            # Uncomment logic if SMTP is configured, otherwise simulate
            # send_mail(subject, msg_body, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL], fail_silently=True)
            pass
        except:
            pass
        
        # Simulate success for demo
        messages.success(request, "Your enquiry has been submitted. We will contact you shortly.")
        
        return redirect('contact')
        
    return render(request, 'enquiries/contact.html', {'company_info': company_info})
