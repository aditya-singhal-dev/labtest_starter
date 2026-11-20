LAB TEST STARTER PROJECT  (Full Stack Development Lab - Assignments 9 & 10)
==========================================================================

SETUP (about 3 minutes)
  1. pip install django            (only if Django is not installed)
  2. python manage.py migrate
  3. python manage.py seed_data    (loads 5 categories, 30 products, 40 orders + 2 users)
  4. python manage.py runserver
  5. Open http://127.0.0.1:8000/

LOGINS
  admin   / Admin@123     (staff user, can open /admin/)
  student / Student@123   (normal user)

WHAT IS GIVEN
  shop/models.py        Category, Product, Order  (do NOT change the models)
  shop/views.py         home, product_list, order_list
  shop/urls.py          /  /products/  /orders/
  labtest/urls.py       /login/  /logout/  /admin/
  templates/base.html   Bootstrap 5 layout + navbar (extend it in every template)
  templates/shop/       home.html, product_list.html, order_list.html

USEFUL FACTS
  - Product -> Category is a ForeignKey:  product.category.name,  filter(category__name__icontains=...)
  - Order -> Product is a ForeignKey:     order.product.name,     Product.objects.annotate(Sum('order__quantity'))
  - Order.status is either "Pending" or "Delivered".
  - Each order row in order_list.html has id="order-<id>" and its status cell has class="status".
  - Running seed_data again resets all products and orders.

Write your roll number on the first line of shop/views.py.
