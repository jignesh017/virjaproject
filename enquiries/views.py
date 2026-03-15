from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Enquiry
from core.models import CompanyInfo
from core.utils import send_custom_email

def contact(request):
    company_info = CompanyInfo.objects.first()
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        company_name = request.POST.get('company_name', '')
        state = request.POST.get('state', '')
        message = request.POST.get('message')

        # Save to DB
        Enquiry.objects.create(name=name, email=email, phone=phone, company_name=company_name, state=state, message=message)

        # Send Email
        subject = f"New Business Enquiry from {name}"
        msg_body = f"Name: {name}\nCompany: {company_name}\nEmail: {email}\nPhone: {phone}\nState: {state}\n\nMessage:\n{message}"
        
        # Get admin email from CompanyInfo
        admin_email = company_info.email if company_info else None
        if admin_email:
            send_custom_email(subject, msg_body, [admin_email])
        
        # Simulate success for demo
        messages.success(request, "Your enquiry has been submitted. We will contact you shortly.")
        
        return redirect('contact')
        
    return render(request, 'enquiries/contact.html', {'company_info': company_info})
