from django.contrib import admin

from .models import Product, CartItem
from .models import Restaurant,Dish
 
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Restaurant)
admin.site.register(Dish)