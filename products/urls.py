from django.urls import path, include
from products.views import index, products

app_name = 'products'

urlpatterns = [
    path('', products, name='index')
]
