from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from products.models import Product, ProductCategory, Basket
from users.models import User
from users.views import login


def index(request):
    context = {
        'title': 'Test Title',
        'is_promotion': False
    }
    return render(request, 'products/index.html', context)

def products(request, category_id=None):
    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()

    context = {
        'title' : 'Store - Каталог',
        'products': products,
        'categories': ProductCategory.objects.all(),
    }

    return render(request, 'products/products.html', context)

@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()


    return HttpResponseRedirect(request.META.get('HTTP_REFERER', ''))

@login_required()
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


