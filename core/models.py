from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    wallet = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return self.username


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    # image = models.ImageField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Purchase(models.Model):
    quantity = models.PositiveIntegerField()
    purchase_datetime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_purchases')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_purchases')


class Refund(models.Model):
    request_datetime = models.DateTimeField(auto_now_add=True)
    purchase = models.OneToOneField(Purchase, on_delete=models.CASCADE, related_name='refund')
