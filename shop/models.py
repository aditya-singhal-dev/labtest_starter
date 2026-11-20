from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=20, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.IntegerField()
    added_on = models.DateField()

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Delivered", "Delivered"),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    order_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")

    def __str__(self):
        return f"{self.customer_name} - {self.product.name}"
