from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from products.models import Product, ProductCategory, Basket
from django.core.paginator import Paginator


def index(request):
    context = {
        'title': 'Test Title',
        'is_promotion': False
    }
    return render(request, 'products/index.html', context)

def products(request, category_id=None):
    PER_PAGE = 1
    if category_id:
        category = ProductCategory.objects.get(id=category_id)
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()
    page = request.GET.get('page', 1)
    if not isinstance(page, int):
        if page.isdigit():
            page = int(page)
        else:
            page = 1
    paginator = Paginator(products, per_page=PER_PAGE)
    page_products = paginator.page(page)
    return render(request, 'products/products.html', context={
        'title': 'Store - продукты',
        'products': page_products,
        'category': ProductCategory.objects.all(),
        'category_id': category_id
    })


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


