from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.template.loader import render_to_string
from core.utils import send_custom_email
from cart.models import Cart

def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

@login_required
@user_passes_test(is_admin, login_url='/dashboard/login/')
def user_carts_list(request):
    # Only get submitted carts
    carts = Cart.objects.filter(is_submitted=True).order_by('-updated_at')
    
    context = {
        'carts': carts,
        'page_title': 'User Carts',
    }
    return render(request, 'dashboard/carts/list.html', context)

@login_required
@user_passes_test(is_admin, login_url='/dashboard/login/')
def user_cart_detail(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id, is_submitted=True)
    
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
                from django.utils import timezone
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
