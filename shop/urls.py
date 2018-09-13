from django.urls import path
from shop import views

urlpatterns = [
    path('', views.home, name='store_home'),

    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<slug:slug>/', views.add_cart, name='cart_add'),
    path('cart/remove/<slug:slug>/', views.cart_remove, name='cart_remove'),

    path('<slug:category>/', views.category, name='category'),
    path('<slug:category>/<slug:item>/', views.item, name='item'),


]
