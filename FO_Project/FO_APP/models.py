from django.db import models
from django.contrib.auth.models import User


class Products(models.Model):

    CATEGORY_CHOICES = [
        ('Not Mentioned', 'Not Mentioned'),
        ('Soups-Veg', 'Soups-Veg'),
        ('Soups-Non Veg', 'Soups-Non Veg'),
        ('Starters-Egg', 'Starters-Egg'),
        ('Starters-Veg', 'Starters-Veg'),
        ('Starters-Non Veg Special', 'Starters_Non Veg Special'),
        ('Non Veg Starters-Chicken', 'Non Veg Starters-Chicken'),
        ('Non Veg Starters-Mutton', 'Non Veg Starters-Mutton'),
        ('SeaFood Starters', 'SeaFood Starters'),
        ('Rice & Noodles-Veg', 'Rice & Noodles-Veg'),
        ('Rice & Noodles-Non Veg', 'Rice & Noodles-Non Veg'),
        ('Rice & Noodles-Egg', 'Rice & Noodles-Egg'),
        ('Veg Gravies', 'Veg Gravies'),
        ('Non Veg Gravies', 'Non Veg Gravies'),
        ('Biriyani Varieties', 'Biriyani Varieties'),
        ('Dosa Varities', 'Dosa Varities'),
        ('Breads', 'Breads'),
        ('MilkShakes', 'MilkShakes'),
        ('Fresh Juices', 'Fresh Juices'),
        ('Desserts', 'Desserts'),
        ('Sodas', 'Sodas'),
    ]

    T_CATEGORY_CHOICES = [
        ('Not Mentioned', 'Not Mentioned'),
        ('All', 'All'),
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
    ]

    name = models.CharField(max_length=100)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')

    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, default='Not Mentioned')
    t_type = models.CharField(
        max_length=50, choices=T_CATEGORY_CHOICES, default='Not Mentioned')

    def __str__(self):
        return self.name


class CartItem(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)


class Dish(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    dish = models.CharField(max_length=255)


class Customer(models.Model):
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.PositiveIntegerField(default=0)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)

    def save(self, *args, **kwargs):
        if not self.user_id and self.user:
            self.user_id = self.user.id
        super(Profile, self).save(*args, **kwargs)
