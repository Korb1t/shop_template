from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from shop_temp.models import *


def homepage(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart.id
    categories = Category.objects.all()
    products = Product.objects.all()
    ctx = {
        'categories': categories,
        'products': products,
        'cart': cart
    }
    return render(request, 'home.html', ctx)


def product_view(request, product_slug):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart.id
        cart = Cart.objects.get(id=cart_id)
    product = Product.objects.get(slug=product_slug)
    ctx = {
        'product': product,
        'cart': cart
    }

    return render(request, 'product.html', ctx)


def category_view(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    products_of_category = Product.objects.filter(category=category)
    ctx = {
        'category': category,
        'products_of_category': products_of_category
    }

    return render(request, 'category.html', ctx)


def cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
        request.session['cart_id'] = cart.id
    ctx = {
        'cart': cart
    }

    return render(request, 'cart.html', ctx)


def add_to_cart_view(request):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
    product_slug = request.GET.get('product_slug')
    product = Product.objects.get(slug=product_slug)
    cart.add_to_cart(product.slug)
    return JsonResponse({'cart_total': cart.items.count()})


def remove_from_cart_view(request, product_slug):
    try:
        cart_id = request.session['cart_id']
        cart = Cart.objects.get(id=cart_id)
        request.session['total'] = cart.items.count()
    except:
        cart = Cart()
        cart.save()
        cart_id = cart.id
    product = Product.objects.get(slug=product_slug)
    cart.remove_from_cart(product.slug)
    return HttpResponseRedirect(reverse('cart'))
