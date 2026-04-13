from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.contrib import messages
from .models import Cart, CartItem
from products.models import Product
from enquiries.models import Enquiry
from core.models import CompanyInfo
from core.utils import send_custom_email

def get_or_create_cart(request):
    if not request.session.session_key:
        request.session.create()
    cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart

@require_POST
def cart_add(request, product_id):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        
    return JsonResponse({'status': 'success', 'cart_items_count': cart.get_total_items()})

@require_POST
def cart_update(request, product_id):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    try:
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        quantity = 1
        
    if quantity > 0:
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity = quantity
        cart_item.save()
    else:
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.delete()
        except CartItem.DoesNotExist:
            pass
            
    return JsonResponse({'status': 'success', 'cart_items_count': cart.get_total_items()})

@require_POST
def cart_remove(request, product_id):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass
        
    return JsonResponse({'status': 'success', 'cart_items_count': cart.get_total_items()})

@require_POST
def cart_decrease(request, product_id):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass
        
    return JsonResponse({'status': 'success', 'cart_items_count': cart.get_total_items()})

def cart_reload(request, cart_id):
    # Retrieve the historical cart and verify it belongs to the session
    submitted_cart_ids = request.session.get('submitted_cart_ids', [])
    if cart_id not in submitted_cart_ids:
        messages.error(request, "Invalid cart reload request.")
        return redirect('cart:cart_detail')
    
    historical_cart = get_object_or_404(Cart, id=cart_id, is_submitted=True)
    active_cart = get_or_create_cart(request)
    
    # Copy items from historical to active
    for item in historical_cart.items.all():
        active_item, created = CartItem.objects.get_or_create(cart=active_cart, product=item.product)
        if created:
            active_item.quantity = item.quantity
        else:
            active_item.quantity += item.quantity
        active_item.save()
        
    messages.success(request, f"Previous quote items loaded into your active cart. You can now modify and submit it.")
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = get_or_create_cart(request)
    company_info = CompanyInfo.objects.first()
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        company_name = request.POST.get('company_name', '')
        state = request.POST.get('state', '')
        city = request.POST.get('city', '')
        base_message = request.POST.get('message', '')
        
        # Build message with cart items
        items_list = "\n".join([f"- {item.quantity} x {item.product.name}" for item in cart.items.all()])
        message = f"{base_message}\n\nRequested Products:\n{items_list}"
        
        # No longer creating an Enquiry. Details are stored directly on the Cart below.
        
        # Send Email
        subject = f"New Quote Request from {name}"
        msg_body = f"Name: {name}\nCompany: {company_name}\nEmail: {email}\nPhone: {phone}\nState: {state}\nCity: {city}\n\nMessage:\n{base_message}\n\nRequested Products:\n{items_list}"
        
        admin_email = company_info.email if company_info else None
        
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
            
        messages.success(request, "Your quote request has been submitted successfully.")
        
        # Link submitter details directly to cart and reset session
        cart.name = name
        cart.email = email
        cart.phone = phone
        cart.company_name = company_name
        cart.state = state
        cart.city = city
        cart.message = message
        
        cart.is_submitted = True
        
        # Add to session history before clearing session key
        submitted_cart_ids = request.session.get('submitted_cart_ids', [])
        submitted_cart_ids.append(cart.id)
        request.session['submitted_cart_ids'] = submitted_cart_ids
        
        cart.session_key = None
        cart.save()
        
        return redirect('cart:cart_detail')
        
    # Fetch history of submitted carts from session
    submitted_cart_ids = request.session.get('submitted_cart_ids', [])
    submitted_carts = Cart.objects.filter(id__in=submitted_cart_ids).order_by('-updated_at')
        
    return render(request, 'cart/cart_detail.html', {'cart': cart, 'company_info': company_info, 'submitted_carts': submitted_carts})
