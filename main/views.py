from django.http import HttpResponse
from django.shortcuts import render

from carts.models import Cart
from goods.models import Categories
from goods.models import Products

from django.core.paginator import Paginator
from django.shortcuts import render

from goods.models import Products
from goods.utils import q_search

def catalog(request, category_slug=None):

    page = request.GET.get('page', 1)
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)

    if category_slug == 'all':
        goods = Products.objects.all()
    elif query:
        goods = q_search(query)
    else:
        goods = Products.objects.filter(category__slug=category_slug)

    if on_sale:
        goods = goods.filter(discount__gt=0)

    if order_by and order_by != "default":
        goods = goods.order_by(order_by)

    paginator = Paginator(goods, 6)
    current_page = paginator.page(int(page))

    context = {
        'title': 'Coffee - Каталог',
        'goods': current_page,
        "slug_url": category_slug,
    }
    return render(request, 'main/index.html', context)

def product(request, product_slug):
    
    product = Products.objects.get(slug=product_slug)

    context = {
        'product': product
    }

    return render(request, 'main/index.html', context)


def index(request, category_slug=None):
    all_products = Products.objects.all()
    cart = Cart.objects.all()
    cart_data = {}
    for item in cart:
        product_id = item.product.id
        cart_data[product_id] = item.quantity

    context = {
        'title': 'Coffee - Главная',
        'products': all_products,
        'cart': cart,
        'cart_data': cart_data,
        'slug_url': category_slug, 
    }

    return render(request, 'main/index.html', context)





def about(request):
    context = {
        'title': 'Home - О нас',
        'content': "О нас",
        'text_on_page': "fsddhkahakfajhfkahfjhh",
    }

    return render(request, 'main/about.html', context)