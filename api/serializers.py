from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db.models import Sum
from . import models


class ProductSerializer(serializers.ModelSerializer):
   class Meta:
      model = models.Product
      fields = "__all__"
      read_only_fields = ["id"]


class SellerCustomerSerializer(serializers.ModelSerializer):
   class Meta:
      model = models.SellerCustomer
      fields = "__all__"
      read_only_fields = ["id"]

   def create(self, validated_data):
      seller_customer, _ = models.SellerCustomer.objects.get_or_create(**validated_data)
      return seller_customer


class PurchaseSerializer(serializers.ModelSerializer):
   class Meta:
      model = models.Purchase
      fields = "__all__"
      read_only_fields = ["id"]
   
   
class ItemSerializer(serializers.ModelSerializer):
   name = serializers.SerializerMethodField("get_name")
   price = serializers.SerializerMethodField("get_price")
   total = serializers.SerializerMethodField("get_total")
   class Meta:
      model = models.Item
      fields = ["id","purchase","product","name","price","quantity","total"]
      read_only_fields = ["id","price","total"]

   def get_name(self, object):
      return models.Product.objects.get(id=object.product.id).name

   def get_price(self, object):
      return models.Product.objects.get(id=object.product.id).price

   def get_total(self, object):
      return models.Product.objects.get(id=object.product.id).price * object.quantity


class PaymentSerializer(serializers.ModelSerializer):
   customer = serializers.SerializerMethodField("get_customer")
   class Meta:
      model = models.Payment
      fields = ["id","seller_customer","customer","datetime","amount"]
      read_only_fields = ["id","customer"]
   
   def get_customer(self, object):
      return get_user_model().objects.get(user_as_customer=object.seller_customer).name


class OrderSerializer(serializers.ModelSerializer):
   customer = serializers.SerializerMethodField("get_customer")
   items = serializers.SerializerMethodField("get_items")
   class Meta:
      model = models.Purchase
      fields = ["id","seller_customer","customer","datetime","amount","status","items"]
      read_only_fields = ["id","customer","items"]

   def get_customer(self, object):
      return get_user_model().objects.get(user_as_customer=object.seller_customer).name

   def get_items(self, object):
      query_set = models.Item.objects.filter(purchase=object.id)
      serializer = ItemSerializer(query_set, many=True)
      return serializer.data


class CustomerSerializer(serializers.ModelSerializer):
   total = serializers.SerializerMethodField("get_total")
   paid = serializers.SerializerMethodField("get_paid")
   class Meta:
      model = get_user_model()
      fields = ["id","name","email","total","paid"]
      read_only_field = ["id","total","paid"]

   def get_total(self, object):
      total = models.Purchase.objects.filter(seller_customer__seller=self.context["user"], seller_customer__customer=object.id).aggregate(Sum("amount"))["amount__sum"]
      return total

   def get_paid(self, object):
      paid = models.Payment.objects.filter(seller_customer__seller=self.context["user"], seller_customer__customer=object.id).aggregate(Sum("amount"))["amount__sum"]
      return paid

