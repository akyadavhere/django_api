from django.db   import models
from user.models import CustomUser

class Sellers_Customers(models.Model):
   seller   = models.ForeignKey(CustomUser, related_name="user_as_seller", on_delete=models.CASCADE)
   customer = models.ForeignKey(CustomUser, related_name="user_as_customer", on_delete=models.CASCADE)


class Products(models.Model):
   seller  = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)
   product = models.CharField(max_length=255)
   price   = models.DecimalField(max_digits=5, decimal_places=2)


class Purchases(models.Model):
   seller_customer = models.ForeignKey(Sellers_Customers, on_delete=models.CASCADE)
   datetime        = models.DateTimeField(auto_now_add=True)
   total           = models.DecimalField(max_digits=8, decimal_places=2)
   state           = models.BooleanField(default=True, null=True)


class Items(models.Model):
   purchase = models.ForeignKey(Purchases, on_delete=models.CASCADE)
   product  = models.ForeignKey(Products, on_delete=models.PROTECT)
   quantity = models.DecimalField(max_digits=5, decimal_places=2)


class Payments(models.Model):
   seller_customer = models.ForeignKey(Sellers_Customers, on_delete=models.CASCADE)
   datetime        = models.DateTimeField(auto_now_add=True)
   amount          = models.IntegerField()

