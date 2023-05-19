from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import Product, Customer, Order, OrderItem, UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


import json
from decimal import Decimal

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and UserProfile.objects.get(user=user).is_Admin == False:
            login(request, user)
            request.session['username'] = username
            next_url = request.POST.get('next', '')
            if next_url == '':
                return redirect('main')
            return redirect(next_url)
    return render(request, 'user_login.html')

def checklogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username,password = password)
        if user is not None and UserProfile.objects.get(user=user).is_Admin == True:
            login(request, user)
            return redirect('admin_product')
        elif user is not None and UserProfile.objects.get(user=user).is_Admin == False:
            request.session['username'] = username
            login(request, user)
            return redirect('main')
        message = 'Tên đăng nhập hoặc mật khẩu không đúng'
        context = {
            'message': message
        }
        return render(request, 'login.html', context)
    return render(request, 'login.html')

def check_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        name = request.POST['name']
        phone = request.POST['phone']
        address = request.POST['address']
        if User.objects.filter(username=username).exists():
            message = 'Tên đăng nhập đã tồn tại'
            context = {
                'message_username': message
            }
            return render(request, 'register.html', context)
        if password == password2:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            customer = Customer.objects.create(user=user, name=name, phone=phone, address=address)
            customer.save()
            userProfile = UserProfile.objects.create(user=user, is_Admin=False)
            userProfile.save()
            user = authenticate(request, username = username,password = password)
            login(request, user)
            request.session['username'] = username
            return redirect('main')
        else:
            message = 'Mật khẩu không khớp'
            context = {
                'message_password': message
            }
            return render(request, 'register.html', context)
    return render(request, 'register.html')

def checklogout(request):
    logout(request)
    return redirect('main')



def index(request):
    products = Product.objects.filter(is_delete=False)
    context = {
        'products': products
    }
    return render(request, 'main.html', context)

def get_product_of_type(request, type):
    products = Product.objects.filter(type=type, is_delete=False)
    context = {
        'products': products
    }
    return render(request, 'main.html', context)

def search_product(request):
    if request.method == 'POST':
        search = request.POST.get('text-search')
        products = Product.objects.filter(name__contains=search, is_delete=False)
        context = {
            'products': products
        }
        return render(request, 'main.html', context)
    else:
        return redirect('main')
    
def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

def cart(request):
    product_ids = request.GET.get('productIds', '').split(',')
    products = Product.objects.filter(id__in=product_ids)
    products_json = json.dumps(list(products.values()), default=decimal_default)
    context = {'products_json': products_json}
    return render(request, 'cart.html', context)

@login_required(login_url='/user_login/')
def order(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            customer = Customer.objects.get(user=request.user)
            
            name = request.POST.get('name', '')
            phone = request.POST.get('phone', '')
            address = request.POST.get('address', '')
            customer.name = name
            customer.phone = phone
            customer.address = address
            customer.save()
            
            # Tính tổng tiền của đơn hàng
            cart = json.loads(request.POST.get('cart_name', '{}'))
            total = 0
            for product_id, quantity in cart.items():
                product = Product.objects.get(id=product_id)
                total += product.price * quantity
            # Tạo đối tượng Order mới
            order = Order.objects.create(customer=customer, address=address, total=total, status='pending')    
            # Tạo các đối tượng OrderItem mới
            for product_id, quantity in cart.items():
                product = Product.objects.get(id=product_id)
                OrderItem.objects.create(order=order, product=product, quantity=quantity, price=product.price)
            return redirect('purchase_history', status='all')
    else:
        customer = Customer.objects.get(user=request.user)
        context = {
            'customer': customer
        }
        return render(request, 'order.html', context)

@login_required(login_url='/user_login/')
def order_history(request, status):
    if request.user.is_authenticated and UserProfile.objects.get(user=request.user).is_Admin == False:
        customer = Customer.objects.get(user=request.user)
        if status == 'all':
            order = Order.objects.filter(customer=customer).order_by('-date')
        else:
            order = Order.objects.filter(customer=customer, status=status).order_by('-date')
        list_order_item = []
        for order_item in order:
            list_order_item.extend(list(OrderItem.objects.filter(order=order_item)))
        context = {
            "customer": customer,
            "order": order,
            "list_order_item": list_order_item
        }
        for i in order:
            print(i.date)
        return render(request, 'order_history.html', context)
    else:
        return redirect('user_login')
    
########################----Admin----###############################

def admin_product(request):
    products = Product.objects.filter(is_delete=False)
    count = Order.objects.filter(status='pending').count()
    context = {
        'products': products,
        'count': count
    }
    return render(request, 'admin_product.html', context)
def search_product_admin(request):
    search = request.GET.get('text-search')
    products = Product.objects.filter(name__contains=search, is_delete=False)
    count = Order.objects.filter(status='pending').count()
    context = {
        'products': products,
        'count': count
    }
    return render(request, 'admin_product.html', context)
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        type = request.POST.get('type', '')
        price = request.POST.get('price', '')
        description = request.POST.get('description', '')
        image = request.FILES.get('image_upload', '')
        product = Product.objects.create(name=name, type=type, price=price, description=description, image=image)
        return redirect('admin_product')
    else:
        return render(request, 'add_product.html')
def delete_product(request, id):
    product = Product.objects.get(id=id)
    product.is_delete = True
    product.save()
    return redirect('admin_product')
def get_infor_update_product(request, id):
    product = Product.objects.get(id=id)
    data = {
        'id': product.id,
        'name': product.name,
        'image': product.image.url,
        'type': product.type,
        'price': product.price,
        'description': product.description,
    }
    return JsonResponse(data)
def update_product(request):
    if request.method == 'POST':
        id = request.POST.get('id_update', '')
        product = Product.objects.get(id=id)
        product.name = request.POST.get('name_update', '')
        product.type = request.POST.get('type_update', '')
        product.price = request.POST.get('price_update', '')
        product.description = request.POST.get('description_update', '')
        image = request.FILES.get('image_update_file', '')
        if image:
            # Xóa ảnh cũ
            product.image.delete(save=False)
            # Lưu ảnh mới
            product.image = image
        product.save()
        return redirect('admin_product')
    else:
        return render(request, 'update_product.html')

    
def admin_order(request):
    orders = Order.objects.filter(status='pending').order_by('-date')
    count = Order.objects.filter(status='pending').count()
    context = {
        'orders': orders,
        'count': count
    }
    return render(request, 'admin_order.html', context)
def order_items(request, order_id):
    items = OrderItem.objects.filter(order_id=order_id)
    data = []
    for item in items:
        data.append({
            'image': item.product.image.url,
            'product_name': item.product.name,
            'quantity': item.quantity,
            'price': item.price
        })
    return JsonResponse(data, safe=False)

def confirm_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.status = 'confirm'
    order.save()
    return redirect('admin_order')
def cancel_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.status = 'cancel'
    order.save()
    return redirect('admin_order')

def admin_order_done(request):
    orders = Order.objects.filter(status='confirm').order_by('-date')
    count = Order.objects.filter(status='pending').count()
    context = {
        'orders': orders,
        'count': count
    }
    return render(request, 'admin_order_done.html', context)
def admin_order_cancel(request):
    orders = Order.objects.filter(status='cancel').order_by('-date')
    count = Order.objects.filter(status='pending').count()
    context = {
        'orders': orders,
        'count': count
    }
    return render(request, 'admin_order_cancel.html', context)

def admin_customer(request):
    customers = Customer.objects.all()
    count = Order.objects.filter(status='pending').count()
    context = {
        'customers': customers,
        'count': count
    }
    return render(request, 'admin_customer.html', context)
def get_infor_customer(request, id):
    customer = Customer.objects.get(id=id)
    data = {
        'id': customer.id,
        'name': customer.name,
        'phone': customer.phone,
        'address': customer.address,
    }
    return JsonResponse(data)
def get_order_customer(request, id):
    orders = Order.objects.filter(customer_id=id).order_by('-date')
    count = Order.objects.filter(status='pending').count()
    context = {
        'orders': orders,
        'count': count
    }
    return render(request, 'admin_customer_order.html', context)

