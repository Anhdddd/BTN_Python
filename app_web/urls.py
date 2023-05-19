from . import views
from django.urls import path

urlpatterns = [
    path('checklogin/', views.checklogin, name='checklogin'),
    path('checklogout/', views.checklogout, name='checklogout'),
    path('check_register/', views.check_register, name='check_register'),
    
    path('', views.index, name='main'),
    path('product/<str:type>', views.get_product_of_type, name='get_product_of_type'),
    path('search/', views.search_product, name='search_product'),
    path('purchase_history/<str:status>', views.order_history, name='purchase_history'),
    path('user_login/', views.user_login, name='user_login'),
    path('cart/', views.cart, name='cart'),
    path('order/', views.order, name='order'),
    
    path('admin_product/', views.admin_product, name='admin_product'),
    path('admin_product/search/', views.search_product_admin, name='search_product_admin'),
    path('admin_product/add/', views.add_product, name='add_product'),
    path('admin_product/delete/<int:id>/', views.delete_product, name='delete_product'),
    path('get_infor_update_product/<int:id>/', views.get_infor_update_product, name='get_infor_update_product'),
    path('update_product/', views.update_product, name='update_product'),
    path('admin_order/', views.admin_order, name='admin_order'),
    path('order_items/<int:order_id>/', views.order_items, name='order_items'),
    path('confirm_order/<int:order_id>/', views.confirm_order, name='confirm_order'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('admin_order_done/', views.admin_order_done, name='admin_order_done'),
    path('admin_order_cancel/', views.admin_order_cancel, name='admin_order_cancel'),
    path('admin_customer/', views.admin_customer, name='admin_customer'),
    path('get_infor_customer/<int:id>/', views.get_infor_customer, name='get_infor_customer'),
    path('get_order_customer/<int:id>', views.get_order_customer, name='get_order_customer'),
]
