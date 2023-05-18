from django.contrib import admin
from .models import Product, Customer, Order, OrderItem, UserProfile
# Register your models here.
class Product_View(admin.ModelAdmin):
    list_display = ("name", "type")
class Customer_View(admin.ModelAdmin):
    list_display = ("name", "phone")
class User_Profile_View(admin.ModelAdmin):
    list_display = ("user", "is_Admin")
admin.site.register(Product, Product_View)
admin.site.register(Customer, Customer_View)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(UserProfile, User_Profile_View)
