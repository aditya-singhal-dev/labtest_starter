# Roll No: ____________
from django.shortcuts import render
from .models import Product, Order


def home(request):
    return render(request, "shop/home.html")


def product_list(request):
    products = Product.objects.select_related("category").all()
    return render(request, "shop/product_list.html", {"products": products})


def order_list(request):
    orders = Order.objects.select_related("product").order_by("-order_date")
    return render(request, "shop/order_list.html", {"orders": orders})
