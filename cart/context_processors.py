from .models import Cart

def cart_count(request):
    if not request.session.session_key:
        request.session.create()
    
    try:
        cart = Cart.objects.get(session_key=request.session.session_key)
        return {'cart_items_count': cart.get_total_items()}
    except Cart.DoesNotExist:
        return {'cart_items_count': 0}
