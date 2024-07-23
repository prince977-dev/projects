from django.shortcuts import render
from shop.models import Product

# Create your views here.
def search(request):
    p=None
    s=''
    if (request.method=='POST'):
        s=request.POST['search']
        if s:
            p=Product.objects.filter(p_name__icontains=s)
    return render(request,'search.html',{'p':p})
