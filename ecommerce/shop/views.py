from django.shortcuts import render
from .models import Category,Product
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect


# Create your views here.
def home(request):
    return render(request,'home.html')
def catagory(request):
    cat=Category.objects.all()
    return render(request,'catagory.html',{'cat':cat})
def product(request,id):
    cat=Category.objects.get(id=id)
    pro=Product.objects.filter(p_category=id)
    return render(request,'product.html',{'cat':cat,'pro':pro})
def productdetails(request,id):
    pro1=Product.objects.get(id=id)
    return render(request,'productdetails.html',{'pro1':pro1})


def user_login(request):
    if(request.method=="POST"):
        usr_name=request.POST['u']
        pwd=request.POST['p']
        user=authenticate(username=usr_name,password=pwd)
        if user:
            login(request,user)
            return redirect('shop:home')
        else:
            messages.error(request,"Invalid Credentials")
    return render(request,'login.html')
def user_logout(request):
    logout(request)
    return redirect('shop:login')


def registration(request):
    if(request.method=='POST'):
        u=request.POST['u']
        p= request.POST['p']
        cp = request.POST['cp']
        fname = request.POST['fname']
        lname= request.POST['lname']
        email=request.POST['email']
        reg=User.objects.create_user(username=u,password=p,first_name=fname,last_name=lname,email=email)
        if p==cp:
            reg.save()
        else:
            messages.error(request,"confirm password must be same as password")


    return render(request,'registration.html')
