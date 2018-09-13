from django.shortcuts import render, get_object_or_404, redirect
from shop.models import Item, Category
from shop.cart import Cart
from shop.forms import CartAddProductForm


def home(request):
    items = Item.objects.all()
    return render(request, 'shop/index.html', {'items': items, 'cart_product_form': CartAddProductForm()})


def category(request, category):
    cat = Category.objects.get(slug=category)
    highlight = cat.items.all().order_by('-rating')[:3]
    return render(request, 'shop/index.html', {'items': cat.items.all(), 'highlight': highlight})


def item(request, category, item):
    item = get_object_or_404(Item, slug=item, category__slug=category)
    return render(request, 'shop/item.html', {'item': item})


def add_cart(request, slug):
    cart = Cart(request)
    item = get_object_or_404(Item, slug=slug)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        clean = form.cleaned_data
        cart.add(item=item, quantity=clean['quantity'], update_quantity=clean['update'])
    return redirect('cart_detail')


def cart_remove(request, slug):
    cart = Cart(request)
    item = get_object_or_404(Item, slug=slug)
    cart.remove(item)
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    print(cart)
    for item in cart:
        print(item)
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'shop/detail.html', {'cart': cart})
