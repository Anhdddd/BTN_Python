from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_Admin = models.BooleanField(default=False)
    
class Product(models.Model):
    PRODUCT_TYPE_CHOICES = (
        ('fish', 'Cá'),
        ('meat', 'Thịt'),
        ('vegetable', 'Rau củ trái cây'),
        ('milk', 'Sữa'),
        ('drink', 'Đồ uống'),
        ('noodel', 'Mì gói'),
        ('snack', 'Bánh kẹo'),
        ('misc', 'Khác')
    )
        
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    type = models.CharField(max_length=255, choices=PRODUCT_TYPE_CHOICES , default='null')

class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, default='null')
    address = models.CharField(max_length=255, default='null')

class Order(models.Model):
    ORDER_STATUS_CHOICES = (
        ('pending', 'Chờ xử lý'),
        ('confirm', 'Đã xác nhận'),
        ('cancel', 'Đã hủy')
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='null')
    phone = models.CharField(max_length=255, default='null')
    address = models.CharField(max_length=255, default='null')
    date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES)
# Lưu sản phẩm đã mua
class OrderItem(models.Model):  
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
