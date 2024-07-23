from django.shortcuts import render,HttpResponse,redirect
from .models import Product,Cart,Payment,Order_details
from django.contrib.auth.models import User
import razorpay
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def add_to_cart(request,id):
    p=Product.objects.get(id=id)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)
        if(p.p_stock>0):
            cart.quantity+=1
            cart.save()
            p.p_stock-=1
            p.save()
    except:
        if (p.p_stock > 0):
            cart = Cart.objects.create(user=u, product=p,quantity=1)

            cart.save()
            p.p_stock -= 1
            p.save()
    return redirect('cart:viewcart')

def viewcart(request):
    u=request.user
    cart=Cart.objects.filter(user=u)
    total=0
    for i in cart:
        total=total+i.quantity*i.product.p_price
    return render(request,'viewcart.html',{'cart':cart,'total':total})

def remove_from_cart(request,id):
    p=Product.objects.get(id=id)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)
        if(cart.quantity>1):
          cart.quantity-=1
          cart.save()
          p.p_stock+=1
          p.save()
        else:
            cart.delete()
            p.p_stock+1
            p.save()
    except:
        pass


    return redirect('cart:viewcart')
def delet_from_cart(request,id):
    p = Product.objects.get(id=id)
    u = request.user
    try:
        cart = Cart.objects.get(user=u, product=p)
        cart.delete()
        p.p_stock+=cart.quantity
        p.save()
    except:
        pass
    return redirect('cart:viewcart')

def place_order(request):
    if(request.method=='POST'):
        ph=request.POST.get('p')
        a = request.POST.get('a')
        pin = request.POST.get('pin')
        u=request.user
        c=Cart.objects.filter(user=u)
        total=0
        for i in c:
            total=total+i.quantity * i.product.p_price
        total=int(total*100)
        print(type(total))
        client=razorpay.Client(auth=('rzp_test_7kdmsrPGYoAenp','7LzrQhHP9huKHDj6ewdBatHd'))
        response_payment = client.order.create(dict(amount=total, currency="INR"))
        print(response_payment)
        order_id=response_payment['id']
        order_status=response_payment['status']
        if order_status=='created':
            p=Payment.objects.create(name=u.username,amount=total,order_id=order_id)
            p.save()
            for i in c:
                o=Order_details.objects.create(user=u,product=i.product,address=a,phone=ph,pin=pin,no_of_items=i.quantity,order_id=order_id)
                o.save()
        response_payment['name']=u.username
        return render(request,'payment.html',{'payment':response_payment})


    return render(request,'placeorder.html')
@csrf_exempt
def payment_status(request,u):
    if(request.method=='POST'):
        response=request.POST#Razorpay response after completing of payment
        # print(response)
        print(u)
        param_dict={
        'razorpay_order_id':response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature'],

        }
        client = razorpay.Client(auth=('rzp_test_7kdmsrPGYoAenp', '7LzrQhHP9huKHDj6ewdBatHd'))
        try:
            status=client.utility.verify_payment_signature(param_dict)
            print(status)
            ord = Payment.objects.get(order_id=response['razorpay_order_id'])
            ord.razorpay_payment_id = response['razorpay_payment_id']
            ord.paid = True
            ord.save()
            u=User.objects.get(username=u)
            c=Cart.objects.filter(user=u)

            o=Order_details.objects.filter(user=u,order_id=response['razorpay_order_id'])
            for i in o:
                i.payment_status='paid'
                i.save()
            c.delete()
            return render(request, 'success.html',{'status':True})

        except:
            return render(request, 'success.html', {'status': False})

    return render(request,'success.html')
def your_orders(request):
    u=request.user
    coustomer=Order_details.objects.filter(user=u,payment_status='paid')
    return render(request,'yourorders.html',{'orders':coustomer})