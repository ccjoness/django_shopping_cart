from django.contrib import admin
from shop.models import Item, ItemImage, User, Category, Review

admin.site.register(Item)
admin.site.register(ItemImage)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Review)