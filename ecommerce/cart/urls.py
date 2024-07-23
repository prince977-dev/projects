from django.urls import path
from . import views
app_name='cart'

urlpatterns = [
    path('addtocart/<int:id>', views.add_to_cart, name='addtocart'),
    path('viewcart', views.viewcart, name='viewcart'),
    path('removecart/<int:id>', views.remove_from_cart, name='removecart'),
    path('deletecart/<int:id>', views.delet_from_cart, name='deletcart'),
    path('placeorder', views.place_order, name='placeorder'),
    path('success/<u>', views.payment_status, name='success'),
    path('yourorders',views.your_orders,name='yourorders')

]
