from django.contrib.auth import get_user_model
from django.db import models


class SellerCustomer(models.Model):
   seller  = models.ForeignKey(get_user_model(), related_name="user_as_seller", on_delete=models.CASCADE)
   customer = models.ForeignKey(get_user_model(), related_name="user_as_customer", on_delete=models.CASCADE)
   unique_together = [['seller', 'customer']]


class Product(models.Model):
   seller = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
   name = models.CharField(max_length=255, unique=True)
   price = models.IntegerField()
   unique_together = [['seller', 'name']]


class Purchase(models.Model):
   seller_customer = models.ForeignKey(SellerCustomer, on_delete=models.CASCADE)
   datetime = models.DateTimeField(auto_now_add=True) # default="2006-10-25 14:30:59"
   amount = models.DecimalField(max_digits=8, decimal_places=2)
   status = models.BooleanField(default=True)


class Item(models.Model):
   purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
   product = models.ForeignKey(Product, on_delete=models.PROTECT)
   quantity = models.DecimalField(max_digits=5, decimal_places=2)


class Payment(models.Model):
   seller_customer = models.ForeignKey(SellerCustomer, on_delete=models.CASCADE)
   datetime = models.DateTimeField(auto_now_add=True)
   amount = models.IntegerField()
