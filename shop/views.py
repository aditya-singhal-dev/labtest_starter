# Roll No: ____________
from django.shortcuts import render
from django.db.models import Q
from .models import Product, Order, Category
from django.http import JsonResponse

from django.db.models import Count, Avg, Min, Max
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST


def home(request):
    return render(request, "shop/home.html")



def product_list(request):

    # Step 1: Get keyword from URL
    q = request.GET.get("q", "")

    # Step 2: Get selected category
    category = request.GET.get("category", "")

    # Step 3: Fetch all products and categories
    products = Product.objects.select_related("category").all()
    categories = Category.objects.all()

    # Step 4: Search by name, SKU or category
    if q:
        products = products.filter(
            Q(name__icontains=q) |
            Q(sku__icontains=q) |
            Q(category__name__icontains=q)
        )

    # Step 5: Filter selected category
    if category:
        products = products.filter(category_id=category)

    # Step 6: Send data to HTML
    return render(request, "shop/product_list.html", {
        "products": products,
        "categories": categories,
        "q": q,
        "selected_category": category
    })



def order_list(request):
    orders = Order.objects.select_related("product").order_by("-order_date")
    return render(request, "shop/order_list.html", {"orders": orders})


def search_api(request):

    # Step 1: Read search keyword
    q = request.GET.get("q", "")

    # Step 2: Search database
    products = Product.objects.filter(
        Q(name__icontains=q) |
        Q(sku__icontains=q) |
        Q(category__name__icontains=q)
    ).order_by("id").values(
        "name",
        "sku",
        "category__name",
        "price"
    )[:10]

    # Step 3: Return JSON
    return JsonResponse(list(products), safe=False)



@login_required
def report(request):

    # Product statistics
    stats = Product.objects.aggregate(
        total_products=Count("id"),
        avg_price=Avg("price"),
        min_price=Min("price"),
        max_price=Max("price")
    )

    # Total orders
    total_orders = Order.objects.aggregate(
        total=Count("id")
    )["total"]

    # Category-wise product count
    categories = Category.objects.annotate(
        product_count=Count("product")
    ).order_by("-product_count")

    # Send data to HTML
    return render(request, "shop/report.html", {
        "stats": stats,
        "total_orders": total_orders,
        "categories": categories
    })




@login_required
@require_POST
def deliver_order(request, id):

    # Step 1: Find order by ID
    order = get_object_or_404(Order, id=id)

    # Step 2: Change status
    order.status = "Delivered"

    # Step 3: Save in database
    order.save()

    # Step 4: Return JSON
    return JsonResponse({
        "id": order.id,
        "status": "Delivered"
    })
