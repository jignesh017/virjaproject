import csv
from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.template.loader import render_to_string
from django.db.models import Q
from django.http import HttpResponse
from django.utils import timezone

from cart.models import Cart
from core.utils import send_custom_email

def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

@login_required
@user_passes_test(is_admin, login_url='/dashboard/login/')
def user_carts_list(request):
    # Only get submitted carts
    carts = Cart.objects.filter(is_submitted=True).order_by('-updated_at')
    
    # Filtering logic
    q = request.GET.get('q')
    status = request.GET.get('status')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if q:
        carts = carts.filter(
            Q(name__icontains=q) |
            Q(email__icontains=q) |
            Q(phone__icontains=q) |
            Q(company_name__icontains=q) |
            Q(city__icontains=q) |
            Q(state__icontains=q)
        )
    
    if status == 'unread':
        carts = carts.filter(is_read=False)
    elif status == 'read':
        carts = carts.filter(is_read=True, is_replied=False)
    elif status == 'replied':
        carts = carts.filter(is_replied=True)

    if date_from:
        carts = carts.filter(updated_at__date__gte=date_from)
    if date_to:
        carts = carts.filter(updated_at__date__lte=date_to)
    
    context = {
        'carts': carts,
        'page_title': 'User Carts',
        'q': q,
        'status': status,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'dashboard/carts/list.html', context)

@login_required
@user_passes_test(is_admin, login_url='/dashboard/login/')
def user_cart_detail(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id, is_submitted=True)
    
    # Mark as read
    if not cart.is_read:
        cart.is_read = True
        cart.save()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'delete':
            cart.delete()
            messages.success(request, 'Quote Request deleted successfully.')
            return redirect('dashboard:dashboard_carts_list')
        elif action == 'reply':
            reply_message = request.POST.get('reply_message')
            if reply_message:
                cart.is_replied = True
                cart.reply_message = reply_message
                cart.replied_at = timezone.now()
                cart.save()
                
                # Send the actual email
                try:
                    subject = f"Re: Your Quote Request for {cart.get_total_items()} items"
                    html_content = render_to_string('dashboard/emails/cart_reply.html', {'cart': cart})
                    # Use a plaintext fallback message
                    text_content = f"Hello {cart.name},\n\nWe have reviewed your quote request. Please see our response below:\n\n{cart.reply_message}\n\nThank you."
                    
                    send_custom_email(subject, text_content, [cart.email], html_message=html_content)
                    messages.success(request, f"Reply sent successfully to {cart.email} via Email!")
                except Exception as e:
                    messages.warning(request, f"Reply saved, but failed to send email. Ensure SMTP is configured. Error: {str(e)}")
                    
            return redirect('dashboard:dashboard_cart_detail', cart_id=cart.id)
            
    context = {
        'cart': cart,
        'page_title': f'Cart Details',
    }
    return render(request, 'dashboard/carts/detail.html', context)

@login_required
@user_passes_test(is_admin, login_url='/dashboard/login/')
def user_cart_delete(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id, is_submitted=True)
    if request.method == 'POST':
        cart.delete()
        messages.success(request, "Quote requested deleted successfully.")
        return redirect('dashboard:dashboard_carts_list')
    return render(request, 'dashboard/catalog/category_confirm_delete.html', {
        'item': cart,
        'type': 'Quote Request',
        'cancel_url': 'dashboard:dashboard_carts_list'
    })

@login_required
@user_passes_test(is_admin, login_url='/dashboard/login/')
def user_carts_export(request):
    carts = Cart.objects.filter(is_submitted=True).order_by('-updated_at')
    
    # Apply same filters for export
    q = request.GET.get('q')
    status = request.GET.get('status')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if q:
        carts = carts.filter(
            Q(name__icontains=q) |
            Q(email__icontains=q) |
            Q(phone__icontains=q) |
            Q(company_name__icontains=q) |
            Q(city__icontains=q) |
            Q(state__icontains=q)
        )
    if status == 'unread':
        carts = carts.filter(is_read=False)
    elif status == 'read':
        carts = carts.filter(is_read=True, is_replied=False)
    elif status == 'replied':
        carts = carts.filter(is_replied=True)
    if date_from:
        carts = carts.filter(updated_at__date__gte=date_from)
    if date_to:
        carts = carts.filter(updated_at__date__lte=date_to)

    today = date.today().strftime('%d-%m-%Y')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="customer_details_{today}.csv"'
    
    writer = csv.writer(response)
    # Only customer details as requested
    writer.writerow(['Date', 'Name', 'Email', 'Phone', 'Company', 'State', 'City'])
    
    for cart in carts:
        writer.writerow([
            cart.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            cart.name,
            cart.email,
            cart.phone,
            cart.company_name,
            cart.state,
            cart.city
        ])
        
    return response
