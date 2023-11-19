from django.contrib import admin

from core.models import Product, Purchase, Refund, User

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(Refund)
