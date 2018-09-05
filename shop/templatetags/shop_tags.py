from django import template
from django.utils.html import mark_safe
from django.template.loader import render_to_string
from shop.models import ItemImage, Item, Category

register = template.Library()


@register.simple_tag
def star_rating(item, text=False):
    html = []
    avg = item.get_star_rating()
    for i in range(int(avg)):
        html.append('&#9733;')
    for r in range(5 - int(avg)):
        html.append('&#9734;')
    if text:
        return mark_safe('<span class="text-warning">{}</span> {} stars'.format(' '.join(html), avg))
    return mark_safe(' '.join(html))


@register.simple_tag
def category():
    return mark_safe(render_to_string('shoptags/_category_nav.html', {'category': Category.objects.all()}))
