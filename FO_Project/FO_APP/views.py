from .models import Products  # Assuming you have a model named Products
# Assuming you have a form named ProductsSearchForm
from .forms import ProductsSearchForm
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Products, CartItem
from datetime import datetime
from .forms import ProductCreateForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile
from django.urls import reverse
from .forms import ProductCreateForm, ProductsSearchForm, ProductsUpdateForm

from django.shortcuts import render
from django.conf import settings
import razorpay

# Initialize Razorpay client
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def payment_page(request):
    currency = 'INR'
    amount = 20000  # Rs. 200

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(
        amount=amount,
        currency=currency,
        payment_capture='0'
    ))

    # order id of newly created order
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'

    # Pass the Razorpay key to the payment form template
    razorpay_key = settings.RAZOR_KEY_ID

    # Context data to be passed to the template
    context = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_amount': amount,
        'currency': currency,
        'callback_url': callback_url,
        'razorpay_key': razorpay_key,  # Pass the Razorpay API key to the template
    }

    return render(request, 'payments/payment_forms.html', context=context)


def homepage(request):
    currency = 'INR'
    amount = 20000  # Rs. 200

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))

    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'

    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url

    return render(request, 'indexx.html', context=context)


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):

    # only accept POST request.
    if request.method == "POST":
        try:

            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                amount = 20000  # Rs. 200
                try:

                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)

                    # render success page on successful caputre of payment
                    return render(request, 'paymentsuccess.html')
                except:

                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:

                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:

            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        # if other than POST request is made.
        return HttpResponseBadRequest()


def list_items(request):
    title = 'List of Items'
    form = ProductsSearchForm(request.POST or None)
    queryset = Products.objects.all()

    # Add options for t_type field
    form.fields['t_type'].choices = [
        ('', 'Select Type'),  # Default empty option
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
    ]

    context = {
        "title": title,
        "queryset": queryset,
        "form": form,
    }

    if request.method == 'POST':
        queryset = Products.objects.filter(
            name__icontains=form['name'].value(),
            t_type__icontains=form['t_type'].value(),
            category__icontains=form['category'].value()
        )
        context = {
            "form": form,
            "queryset": queryset,
        }

    return render(request, "list_items.html", context)


def update_items(request, pk):
    queryset = Products.objects.get(id=pk)
    form = ProductsUpdateForm(instance=queryset)
    if request.method == 'POST':
        form = ProductsUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            return redirect('/list_items')
    context = {
        'form': form
    }
    return render(request, 'add_items.html', context)


def delete_items(request, pk):
    queryset = Products.objects.get(id=pk)
    if request.method == 'POST':
        queryset.delete()
        return redirect('/list_items')
    return render(request, 'delete_items.html')


def profiles(request):
    profiles = Profile.objects.all()
    return render(request, 'profiles.html', {'profiles': profiles})


def display_profiles(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        # Redirect to the 'create_profile' URL
        return redirect(reverse('create_profile'))

    context = {
        'user_profile': user_profile,
    }

    return render(request, 'display_profiles.html', context)


def my_view(request):
    current_datetime_python = datetime.now()

    return render(request, 'my_template.html', {'dt': current_datetime_python})


def create_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('display_profiles')  # Define this URL
    else:
        form = ProfileForm()
    return render(request, 'create_profile.html', {'form': form})


def profile_created(request):
    return render(request, 'profile_created.html')


def add_items(request):
    if request.method == 'POST':
        form = ProductCreateForm(request.POST)
        if form.is_valid():
            new_category = form.cleaned_data.get('new_category')
            if new_category:
                # Add the new category to the choices
                Products.CATEGORY_CHOICES.append((new_category, new_category))

            form.save()
            return redirect('/menu')
    else:
        form = ProductCreateForm()

    context = {
        "form": form,
        "title": "Add Item",
    }
    return render(request, "add_items.html", context)


def authView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("index")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


def product_list(request):
    products = Products.objects.all()
    return render(request, 'menu.html', {'products': products})


def add_to_cart(request, product_id):
    product = Products.objects.get(id=product_id)
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


def remove_from_cart(request, product_id):
    product = Products.objects.get(id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product)
        # If the item exists, increment the quantity
        cart_item.quantity -= 1
        cart_item.save()
    except CartItem.DoesNotExist:
        # If the item does not exist, create a new cart item
        cart_item = CartItem(product=product)
        cart_item.save()
    return redirect('cart:view_cart')

# Create your views here.


@login_required
def index(request):
    username = request.user.username
    return render(request, 'index.html', {'username': username})


def menu(request):

    list = Products.objects.all()
    current_datetime_python = datetime.now()
    return render(request, 'menu.html', {'list': list, 'dt': current_datetime_python})


def reservavtion(request):
    return render(request, 'reservation.html', {})


def blog(request):
    return render(request, 'blog.html', {})


def blog_detail(request):
    return render(request, 'blog-detail.html', {})


def about(request):
    return render(request, 'about.html', {})


def login(request):
    return render(request, 'login.html', {})


def regs(request):
    return render(request, 'regs.html', {})


def contact(request):
    return render(request, 'contact.html', {})


def track(request):
    cart_items = CartItem.objects.all()
    item_prices = [int(item.product.price * item.quantity)
                   for item in cart_items]
    total_price = sum(item_prices)
    current_datetime_python = datetime.now()
    item_data = zip(cart_items, item_prices)

    return render(request, 'ot.html', {'item_data': item_data, 'total_price': total_price, 'dt': current_datetime_python})


def regs(request):
    return render(request, 'regs.html', {})


def cart(request):
    cart_items = CartItem.objects.all()
    total_price = sum(item.product.price *
                      item.quantity for item in cart_items)
    total_entries = cart_items.count()
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price, 'total_entries': total_entries})


def item(request):
    return render(request, 'item.html')


def additem(request):
    return render(request, 'additem.html')
