from .models import Profile
from django import forms
from .models import Products


class PaymentForm(forms.Form):
    amount = forms.DecimalField(label='Amount', required=True)
    currency = forms.CharField(label='Currency', initial='INR', required=True)
    razorpay_payment_id = forms.CharField(widget=forms.HiddenInput())


class ProductCreateForm(forms.ModelForm):
    new_category = forms.CharField(
        max_length=100, required=False, label='New Category')

    class Meta:
        model = Products
        fields = ['name', 'price', 'category', 't_type']


# forms.py


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['email', 'address', 'phone_number']


class ProductsSearchForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'price', 'category', 't_type']


class ProductsUpdateForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['name', 'price', 'category', 't_type']
