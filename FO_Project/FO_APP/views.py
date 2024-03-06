from django.shortcuts import render, redirect

from .models import Product, CartItem
 
def product_list(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})
 
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item= CartItem(product=product,user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')
 
def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('cart:view_cart')

# Create your views here.
def index(request):
    return render(request,'index.html',{})

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
    return render(request,'ot.html',{})

def login(request):
    return render(request,'accounts\\login.html',{})

def register(request):
    return render(request,'accounts\\register.html',{})

def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    total_entries = cart_items.count()
    
    print("cart items\n ",cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price, 'total_entries':total_entries})

def item(request):
    return render(request, 'item.html')

def additem(request):
    return render(request, 'additem.html')