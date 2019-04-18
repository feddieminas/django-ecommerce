from django.shortcuts import get_object_or_404
from products.models import Product


def cart_contexts(request):
    """
    Ensures that the cart contents are available when rendering every page
    """
    
    cart = request.session.get('cart', {}) # cart requests a session to be available to all pages
    # it requests the existing cart if there is one, or a blank dict if there is not
    
    # initialize variables
    cart_items=[]
    total = 0
    product_count = 0
    for id, quantity in cart.items(): # product unique id, how much qty wish to purchase
        product = get_object_or_404(Product, pk=id)
        total += quantity * product.price
        product_count += quantity
        cart_items.append({'id': id, 'quantity': quantity, 'product': product})
        
    return {'cart_items': cart_items, 'total': total, 'product_count': product_count}    
    
        