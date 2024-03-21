from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from . import views
from .views import authView

# Import payment_page view function
from .views import payment_page
from . import views  # Import views module from the same directory


urlpatterns = [
    path('', views.index, name='index'),
    path('menu', views.menu, name='menu'),
    path('my_view', views.my_view, name='my_view'),
    path('reservation', views.reservavtion, name='reservation'),
    path('blog', views.blog, name='blog'),
    path('blog-detail', views.blog_detail, name='blog_detail'),
    path('item', views.item, name='item'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('track', views.track, name='track'),
    path('regs', views.regs, name='regs'),
    path('cart', views.cart, name='cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('list_items/', views.list_items, name='list_items'),
    path('add_items/', views.add_items, name='add_items'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('signup/', authView, name='authView'),
    path('create-profile/', views.create_profile, name='create_profile'),
    path('profile-created/', views.profile_created, name='profile_created'),
    path('display-profiles/', views.display_profiles, name='display_profiles'),
    path('profiles/', views.profiles, name='profiles'),
    path('update_items/<str:pk>/', views.update_items, name="update_items"),
    path('delete_items/<str:pk>/', views.delete_items, name="delete_items"),
    path('payment/', views.payment_page, name='payment_page'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
