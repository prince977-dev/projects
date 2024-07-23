from django.contrib import admin
from .models import Cart,Payment,Order_details

# Register your models here.
admin.site.register(Cart)
admin.site.register(Order_details)
admin.site.register(Payment)


