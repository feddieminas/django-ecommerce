from django.shortcuts import render
from products.models import Product

# Create your views here.
def do_search(request):
    products = Product.objects.filter(name__icontains=request.GET['q']) # give form a name of q and ret whatever q there
    return render(request, "products.html", {"products": products})    
    
    
    
