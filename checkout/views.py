from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MakePaymentForm, OrderForm
from .models import OrderLineItem
from django.conf import settings
from django.utils import timezone
from products.models import Product
import stripe

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET

@login_required
def checkout(request):
    if request.method == "POST":
        order_form = OrderForm(request.POST)
        payment_form = MakePaymentForm(request.POST)
        
        if order_form.is_valid() and payment_form.is_valid():
            order = order_form.save(commit=False) 
            order.date = timezone.now()
            order.save()
            
            cart = request.session.get('cart', {}) # get info of what is purchased from current session
            total = 0
            for id, quantity in cart.items():
                product = get_object_or_404(Product, pk=id) # get product id from product purchased
                total += quantity * product.price
                order_line_item = OrderLineItem(
                    order = order,
                    product = product,
                    quantity = quantity
                    )
                order_line_item.save() # details of what is being purchased  
            
            # now we know what we want to buy    
            try:
                customer = stripe.Charge.create( # create a customer charge
                    amount = int(total * 100), # need to multiply as Stripe use cents. ex. 10 euro = 1000 cents
                    currency = "EUR",
                    description = request.user.email,
                    card = payment_form.cleaned_data['stripe_id'], # get the Stripe id, the hidden one from the user
                )
            except stripe.error.CardError:
                messages.error(request, "Your card was declined!") # infrom customer if stg wrong in the process
                
            if customer.paid:
                messages.error(request, "You have succesfully paid")
                request.session['cart'] = {}
                return redirect(reverse('products'))
            else:
                messages.error(request, "Unable to take payment")
        
        else:
            print(payment_form.errors)
            messages.error(request, "We were unable to take a payment with that card!")
            
    else:
        payment_form = MakePaymentForm()
        order_form = OrderForm()
        
    return  render(request, "checkout.html", {'order_form': order_form, 'payment_form': payment_form, 'publishable': settings.STRIPE_PUBLISHABLE})   
        
                
                
                
                
                
                
            
            