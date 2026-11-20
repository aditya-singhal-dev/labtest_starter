from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("products/", views.product_list, name="product_list"),
    path("orders/", views.order_list, name="order_list"),
    path("api/products/search/",views.search_api,name="search_api"),
    path("report/", views.report, name="report"),
    path("api/orders/<int:id>/deliver/",views.deliver_order,name="deliver_order"),
]
