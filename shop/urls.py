from django.urls import path
from shop import views

urlpatterns = [
    path('', views.home, name='store_home'),
    path('<slug:category>/', views.category, name='category'),
    path('<slug:category>/<slug:item>/', views.item, name='item'),
]
