from django.db import models

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.FloatField()
    quantity = models.IntegerField()

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')])
    total_price = models.FloatField()
    products = models.ManyToManyField(Product)
    is_deleted = models.BooleanField(default=False)
