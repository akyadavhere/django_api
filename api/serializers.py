from dataclasses import fields
from datetime import datetime
from rest_framework import serializers
from django.contrib.auth import get_user_model
from . import models

class Sellers_Customers(serializers.ModelSerializer):
   class Meta:
      model = models.Sellers_Customers
      fields = ["id","seller","customer"]
      read_only_fields = ["id"]


class Products(serializers.ModelSerializer):
   class Meta:
      model = models.Products
      fields = ["id","product","price"]
      read_only_fields = ["id"]


class Purchases(serializers.ModelSerializer):
   seller_customer = Sellers_Customers()

   class Meta:
      model = models.Purchases
      fields = ["id","seller_customer","datetime","total","state"]
      read_only_fields = ["id","datetime"]

   def create(self, validated_data):
      
      return super().create(validated_data)

class Items(serializers.ModelSerializer):
   purchase = Purchases()

   class Meta:
      model = models.Items
      fields = ["id","purchase","product","quantity"]

   def create(self, validated_data):
      seller = serializers.CurrentUserDefault()
      total = validated_data.pop("total")
      email = validated_data.pop("email")
      customer = get_user_model().objects.filter(email=email).id
      seller_customer,created = models.Sellers_Customers.objects.get_or_create(seller=seller, customer=customer)

      serializer = Purchases(seller_customer=seller_customer.id, total=total)


      return super().create(validated_data)


