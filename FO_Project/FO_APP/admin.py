from django.contrib import admin

from .models import Products, CartItem
from .models import Restaurant, Dish, Profile
from .forms import ProductCreateForm


class ProductCreateAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 't_type']

    form = ProductCreateForm


admin.site.register(Products, ProductCreateAdmin)
admin.site.register(CartItem)
admin.site.register(Restaurant)
admin.site.register(Dish)
admin.site.register(Profile)
