from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
        city = request.POST.get('city', '')
        message = request.POST.get('message')

        # Save to DB
        Enquiry.objects.create(name=name, email=email, phone=phone, company_name=company_name, state=state, city=city, message=message)

        # Send Email
        subject = f"New Business Enquiry from {name}"
        msg_body = f"Name: {name}\nCompany: {company_name}\nEmail: {email}\nPhone: {phone}\nState: {state}\nCity: {city}\n\nMessage:\n{message}"
        
        # Get admin email from CompanyInfo
        admin_email = company_info.email if company_info else None
        
        # Prepare HTML Email
        html_content = render_to_string('enquiries/emails/admin_notification.html', {
            'name': name,
            'email': email,
            'phone': phone,
            'company_name': company_name,
            'state': state,
            'city': city,
            'message': message
        })
        
        if admin_email:
            send_custom_email(subject, msg_body, [admin_email], html_message=html_content)
        
        # Simulate success for demo
        messages.success(request, "Your enquiry has been submitted. We will contact you shortly.")
        
        return redirect('contact')
        
    return render(request, 'enquiries/contact.html', {'company_info': company_info})

@csrf_exempt
def capture_download_lead(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        company_name = request.POST.get('company_name', '')
        item_title = request.POST.get('item_title', 'Unknown Item')
        item_type = request.POST.get('item_type', 'Catalog/Pricelist')
        
        if not name or not email or not phone:
            return JsonResponse({'status': 'error', 'message': 'Please fill all required fields.'}, status=400)
            
        message = f"Downloaded {item_type}: {item_title}"
        Enquiry.objects.create(
            name=name,
            email=email,
            phone=phone,
            company_name=company_name,
            message=message
        )
        return JsonResponse({'status': 'success', 'message': 'Lead captured successfully'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)
