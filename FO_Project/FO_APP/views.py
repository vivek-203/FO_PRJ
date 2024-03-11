from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Product, CartItem
from datetime import datetime
 
def product_list(request):
    products = Product.objects.all()
    return render(request, 'menu.html', {'products': products})
 
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product)
        # If the item exists, increment the quantity
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        # If the item does not exist, create a new cart item
        cart_item = CartItem(product=product)
        cart_item.save()
    # cart_item = CartItem(product=product)
    # cart_item.save()
    return redirect('menu')
 
def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('cart:view_cart')

# Create your views here.
def index(request):
    username = request.user.username
    return render(request, 'index.html', {'username': username})

def menu(request):
    
    list=Product.objects.all()
    
    return render(request,'menu.html',{'list':list})

def reservavtion(request):
    return render(request,'reservation.html',{})

def blog(request):
    return render(request,'blog.html',{})

def blog_detail(request):
    return render(request,'blog-detail.html',{})

def about(request):
    return render(request,'about.html',{})

def login(request):
    return render(request,'login.html',{})

def regs(request):
    return render(request,'regs.html',{})

def contact(request):
    return render(request,'contact.html',{})

def track(request):
    cart_items = CartItem.objects.all()
    item_prices = [int(item.product.price * item.quantity) for item in cart_items]
    total_price = sum(item_prices)
    current_datetime_python = datetime.now()
    # Zip cart_items and item_prices together
    item_data = zip(cart_items, item_prices)
    
    return render(request, 'ot.html', {'item_data': item_data, 'total_price': total_price, 'dt':current_datetime_python})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to index.html or any other page you want to show the user profile
            return redirect('index')
        else:
            # Return an invalid login error message
            return render(request, 'login.html', {'error_message': 'Invalid login'})
    else:
        return render(request, 'login.html')
def regs(request):
    return render(request,'regs.html',{})

def cart(request):
    cart_items = CartItem.objects.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    total_entries = cart_items.count()
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price, 'total_entries': total_entries})

def item(request):
    return render(request, 'item.html')

def additem(request):
    return render(request, 'additem.html')