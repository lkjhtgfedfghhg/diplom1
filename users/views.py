from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.db.models import Prefetch, Sum
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from carts.models import Cart
from goods.models import Categories, Products
from orders.models import Order, OrderItem

from users.forms import ProfileForm, UserLoginForm, UserRegistrationForm
from users.models import User

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)

            session_key = request.session.session_key

            if user:
                auth.login(request, user)
                messages.success(request, f"{username}, Вы вошли в аккаунт")

                if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user)

                redirect_page = request.POST.get('next', None)
                if redirect_page and redirect_page != reverse('user:logout'):
                    return HttpResponseRedirect(request.POST.get('next'))
                    
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserLoginForm()

    context = {
        'title': 'Coffee - Авторизация',
        'form': form
    }
    return render(request, 'users/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()

            session_key = request.session.session_key

            user = form.instance
            auth.login(request, user)

            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)
            messages.success(request, f"{user.username}, Вы успешно зарегистрированы и вошли в аккаунт")
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()
    
    context = {
        'title': 'Coffee - Регистрация',
        'form': form
    }
    return render(request, 'users/registration.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Профайл успешно обновлен")
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = ProfileForm(instance=request.user)

    orders = Order.objects.filter(user=request.user).prefetch_related(
                Prefetch(
                    "orderitem_set",
                    queryset=OrderItem.objects.select_related("product"),
                )
            ).order_by("-id")
        

    context = {
        'title': 'Coffee - Кабинет',
        'form': form,
        'orders': orders,
    }
    return render(request, 'users/profile.html', context)

def users_cart(request):
    return render(request, 'users/users-cart.html')

def admin_panel(request):
    orders = Order.objects.all().prefetch_related(
        Prefetch(
            "orderitem_set",
            queryset=OrderItem.objects.select_related("order", "product"),
        )
    ).order_by("-id")

    products = Products.objects.all()
    users = User.objects.all()
    order_items = OrderItem.objects.all()

    context = {
        'title': 'Coffee - Управление',
        'orders': orders,
        'dates': [order.created_timestamp for order in orders],
        'deliveries': [order.delivery_address for order in orders],
        'payments_on_delivery': [order.payment_on_get for order in orders],
        'paids': [order.is_paid for order in orders],
        'users': [order.user for order in orders],
        'products': products,
        'users': users,
        'order_items': order_items,
    }
    return render(request, 'users/admin-panel.html', context)



def add_panel(request):
    if request.method == 'POST':
        user_name = request.POST.get('user')
        user = User.objects.get(username=user_name)

        delivery_address = request.POST.get('address')
        status = request.POST.get('status')
        table_number = request.POST.get('table_number')
        
        payment_on_get = request.POST.get('payment_on_get', False)
        is_paid = request.POST.get('is_paid', False)
        
        if payment_on_get == 'True':
            payment_on_get = True
        else:
            payment_on_get = False
        
        if is_paid == 'True':
            is_paid = True
        else:
            is_paid = False

        order = Order(user=user, delivery_address=delivery_address, status=status, payment_on_get=payment_on_get, is_paid=is_paid, table_number=table_number)
        order.save()
        
    return render(request, 'users/add-panel.html')

def edit_sold(request, order_item_id):
  order_item = get_object_or_404(OrderItem, pk=order_item_id)

  if request.method == 'POST':
    name = request.POST.get('address')
    quantity = request.POST.get('table_number')

    order_item.product.name = name  
    order_item.quantity = quantity
    order_item.save()

  return render(request, 'users/edit_sold.html', {'order_item': order_item})


def delete_sold(request, order_item_id):
    sold = get_object_or_404(OrderItem, id=order_item_id)
      
    sold.delete()
    
    return redirect('users:admin-panel')

def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        image = request.FILES.get('image')
        is_staff = request.POST.get('is_staff', False)

        if is_staff == 'True':
            is_staff = True
        else:
            is_staff = False

        user = User(username=username, first_name=first_name, last_name=last_name, image=image, email=email, is_staff=is_staff)
        user.save()

    return render(request, 'users/add_user.html')

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    user.delete()
    
    return redirect('users:admin-panel')

def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        image = request.FILES.get('image')
        is_staff = request.POST.get('is_staff', False)

        if is_staff == 'True':
            is_staff = True
        else:
            is_staff = False

        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.image = image
        user.is_staff = is_staff

        user.save()

        return redirect('users:admin-panel')

    return render(request, 'users/edit_user.html', {'user': user})

def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        price = request.POST.get('price')
        discount = request.POST.get('discount')
        quantity = request.POST.get('quantity')
        category_name = request.POST.get('category')

        category = Categories.objects.get(name=category_name)

        product = Products(name=name, slug=slug, description=description, image=image, price=price, discount=discount, quantity=quantity, category=category)
        product.save()

    return render(request, 'users/add_product.html')


def delete_product(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    
    if product.image:
        product.image.delete()
    
    product.delete()
    
    return redirect('users:admin-panel')

def edit_product(request, product_id):
    product = get_object_or_404(Products, id=product_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        slug = request.POST.get('slug')
        description = request.POST.get('description')
        price = request.POST.get('price')
        discount = request.POST.get('discount')
        quantity = request.POST.get('quantity')
        category_name = request.POST.get('category')

        category = Categories.objects.get(name=category_name)

        product.name = name
        product.slug = slug
        product.description = description
        product.price = price
        product.discount = discount
        product.quantity = quantity
        product.category = category
        product.image=image

        product.save()

        return HttpResponseRedirect(reverse('users:admin-panel')) 

    return render(request, 'users/edit_product.html', {'product': product})

def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('name')
        category_slug = request.POST.get('slug')

        category = Categories(name=category_name, slug=category_slug)  
        category.save() 
    
    return render(request, 'users/add_category.html')

def delete_category(request, category_name):
    category = Categories.objects.get(name=category_name)
    category.delete()
    return redirect('users:admin-panel')

def edit_category(request, category_name):
    category = get_object_or_404(Categories, name=category_name)

    if request.method == 'POST':
        name = request.POST.get('name') 
        slug = request.POST.get('slug')

        category.name = name
        category.slug = slug

        category.save() 

    return render(request, 'users/edit_category.html', {'category': category})


def edit_panel(request, order_id, user_id):
    order = get_object_or_404(Order, id=order_id)
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        delivery_address = request.POST.get('address')
        status = request.POST.get('status', 'Принято')
        table_number = request.POST.get('table_number') 

        payment_on_get = request.POST.get('payment_on_get', False)
        is_paid = request.POST.get('is_paid', False)

        payment_on_get = payment_on_get in ('True', 'true', '1', True)
        is_paid = is_paid in ('True', 'true', '1', True)

        order.user = user
        order.delivery_address = delivery_address
        order.status = status
        order.payment_on_get = payment_on_get
        order.is_paid = is_paid
        order.table_number = table_number

        order.save()

    return render(request, 'users/edit-panel.html', {
        'order': order,
        'user': user,
    })


def delete_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.delete()
    return redirect('users:admin-panel')


@login_required
def logout(request):
    messages.success(request, f"{request.user.username}, Вы вышли из аккаунта")
    auth.logout(request)
    return redirect(reverse('main:index'))