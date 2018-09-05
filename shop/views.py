from django.shortcuts import render, get_object_or_404
from shop.models import Item, Category


def home(request):
    items = Item.objects.all()
    return render(request, 'shop/index.html', {'items': items})


def category(request, category):
    cat = Category.objects.get(slug=category)
    highlight = cat.items.all().order_by('-rating')[:3]
    return render(request, 'shop/index.html', {'items': cat.items.all(), 'highlight': highlight})


def item(request, category, item):
    item = get_object_or_404(Item, slug=item, category__slug=category)
    return render(request, 'shop/item.html', {'item': item})
