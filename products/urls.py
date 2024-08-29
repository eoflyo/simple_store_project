from django.urls import path, include
from products.views import index, products, basket_add, basket_remove

app_name = 'products'

urlpatterns = [
    path('', products, name='index'),
    path('page/<int:page_number>', products, name='paginator'),
    path('category/<int:category_id>/', products, name='category'),
    path('baskets/add/<int:product_id>/', basket_add, name='basket_add'),
    path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
]
