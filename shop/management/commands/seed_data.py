"""Fill the database with sample data. Run: python manage.py seed_data
Order dates are set relative to today, so date-based questions always have data."""
import random
from datetime import date, timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from shop.models import Category, Order, Product

PRODUCTS = [
    # name, sku, category, price, stock
    ("ProSound Wireless Earbuds", "EL-101", "Electronics", 2499, 40),
    ("ProView 24 inch Monitor", "EL-102", "Electronics", 12999, 12),
    ("Smart LED Bulb", "EL-103", "Electronics", 699, 120),
    ("Bluetooth Speaker Mini", "EL-104", "Electronics", 1799, 35),
    ("USB-C Fast Charger", "EL-105", "Electronics", 999, 80),
    ("Wireless Mouse Pro", "EL-106", "Electronics", 1299, 60),
    ("Mechanical Keyboard", "EL-107", "Electronics", 4599, 18),
    ("Python Programming Basics", "BK-201", "Books", 450, 50),
    ("Django for Professionals", "BK-202", "Books", 799, 25),
    ("Data Structures in C", "BK-203", "Books", 520, 30),
    ("Web Development with JavaScript", "BK-204", "Books", 650, 22),
    ("Database System Concepts", "BK-205", "Books", 899, 15),
    ("Problem Solving with Algorithms", "BK-206", "Books", 575, 28),
    ("Cotton Round Neck T-Shirt", "CL-301", "Clothing", 399, 150),
    ("Denim Jacket", "CL-302", "Clothing", 2199, 20),
    ("Formal Shirt Slim Fit", "CL-303", "Clothing", 1199, 45),
    ("Running Shorts", "CL-304", "Clothing", 549, 70),
    ("Winter Hoodie", "CL-305", "Clothing", 1499, 33),
    ("Cricket Bat English Willow", "SP-401", "Sports", 5499, 8),
    ("Football Size 5", "SP-402", "Sports", 899, 40),
    ("Yoga Mat Pro Grip", "SP-403", "Sports", 1099, 55),
    ("Badminton Racket Set", "SP-404", "Sports", 1899, 26),
    ("Skipping Rope", "SP-405", "Sports", 249, 90),
    ("Protein Shaker Bottle", "SP-406", "Sports", 349, 75),
    ("Non-Stick Frying Pan", "HK-501", "Home & Kitchen", 1299, 30),
    ("Electric Kettle 1.5L", "HK-502", "Home & Kitchen", 1599, 24),
    ("Stainless Steel Water Bottle", "HK-503", "Home & Kitchen", 599, 100),
    ("Pressure Cooker 5L", "HK-504", "Home & Kitchen", 2799, 14),
    ("Mixer Grinder Pro 750W", "HK-505", "Home & Kitchen", 3999, 10),
    ("Wall Clock Classic", "HK-506", "Home & Kitchen", 749, 38),
]

CUSTOMERS = [
    "Aarav Sharma", "Diya Patel", "Rohan Gupta", "Ananya Singh", "Kabir Verma",
    "Isha Mehta", "Vivaan Joshi", "Sara Khan", "Arjun Nair", "Meera Iyer",
    "Kunal Bansal", "Priya Reddy",
]


class Command(BaseCommand):
    help = "Delete existing data and load sample categories, products, orders and users."

    def handle(self, *args, **options):
        rng = random.Random(42)
        today = date.today()

        Order.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()

        categories = {}
        for name, sku, cat, price, stock in PRODUCTS:
            if cat not in categories:
                categories[cat] = Category.objects.create(name=cat)

        products = []
        for i, (name, sku, cat, price, stock) in enumerate(PRODUCTS):
            products.append(Product.objects.create(
                name=name, sku=sku, category=categories[cat], price=price,
                stock=stock, added_on=today - timedelta(days=200 - i * 6),
            ))

        # 40 orders spread over the last 60 days.
        # Orders older than 20 days are mostly Delivered; recent ones mostly Pending.
        for i in range(40):
            days_ago = rng.randint(0, 60)
            if days_ago <= 7:
                status = "Pending"
            elif days_ago <= 20:
                status = rng.choice(["Pending", "Pending", "Delivered"])
            else:
                status = rng.choice(["Pending", "Delivered", "Delivered", "Delivered"])
            Order.objects.create(
                product=rng.choice(products[:20] if i % 3 else products),
                customer_name=rng.choice(CUSTOMERS),
                quantity=rng.randint(1, 5),
                order_date=today - timedelta(days=days_ago),
                status=status,
            )

        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "", "Admin@123")
        if not User.objects.filter(username="student").exists():
            User.objects.create_user("student", "", "Student@123")

        self.stdout.write(self.style.SUCCESS(
            f"Loaded {Category.objects.count()} categories, {Product.objects.count()} products, "
            f"{Order.objects.count()} orders. Users: admin (staff), student (normal)."
        ))
