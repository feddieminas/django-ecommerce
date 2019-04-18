from django.shortcuts import render
from .models import Product

# Create your views here.
def all_products(request):
    products = Product.objects.all() # return all products that are in db
    return render(request, "products.html", {"products": products})
    
    