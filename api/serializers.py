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

   def get_name(self, obj):
      return models.Product.objects.get(id=obj.product.id).name

   def get_price(self, obj):
      return models.Product.objects.get(id=obj.product.id).price

   def get_total(self, obj):
      return models.Product.objects.get(id=obj.product.id).price * obj.quantity


class PaymentSerializer(serializers.ModelSerializer):
   opposite_role = serializers.SerializerMethodField("get_opposite_role")
   class Meta:
      model = models.Payment
      fields = ["id","seller_customer","opposite_role","datetime","amount"]
      read_only_fields = ["id","opposite_role"]
   
   def get_opposite_role(self, obj):
      if self.context:
         if self.context["current_url"] == "seller":
            filters = {"user_as_customer": obj.seller_customer}
         else:
            filters = {"user_as_seller": obj.seller_customer}
      else:
         filters = {"user_as_customer": obj.seller_customer}
      return get_user_model().objects.get(**filters).name


class OrderSerializer(serializers.ModelSerializer):
   opposite_role = serializers.SerializerMethodField("get_opposite_role")
   items = serializers.SerializerMethodField("get_items")
   class Meta:
      model = models.Purchase
      fields = ["id","seller_customer","opposite_role","datetime","amount","status","items"]
      read_only_fields = ["id","opposite_role","items"]

   def get_opposite_role(self, obj):
      if self.context["current_url"] == "seller":
         filters = {"user_as_customer": obj.seller_customer}
      else:
         filters = {"user_as_seller": obj.seller_customer}
      return get_user_model().objects.get(**filters).name

   def get_items(self, obj):
      query_set = models.Item.objects.filter(purchase=obj.id)
      serializer = ItemSerializer(query_set, many=True)
      return serializer.data


class CustomerSerializer(serializers.ModelSerializer):
   total = serializers.SerializerMethodField("get_total")
   paid = serializers.SerializerMethodField("get_paid")
   class Meta:
      model = get_user_model()
      fields = ["id","name","email","total","paid"]
      read_only_field = ["id","total","paid"]

   def get_total(self, obj):
      if self.context["current_url"] == "seller":
         filters = {
            "seller_customer__seller": self.context["user"].id,
            "seller_customer__customer": obj.id,
            }
      else:
         filters = {
            "seller_customer__customer": self.context["user"].id,
            "seller_customer__seller": obj.id,
         }
      total = models.Purchase.objects.filter(**filters, status=True).aggregate(Sum("amount"))["amount__sum"]
      return total

   def get_paid(self, obj):
      if self.context["current_url"] == "seller":
         filters = {
            "seller_customer__seller": self.context["user"].id,
            "seller_customer__customer": obj.id,
            }
      else:
         filters = {
            "seller_customer__customer": self.context["user"].id,
            "seller_customer__seller": obj.id,
         }
      paid = models.Payment.objects.filter(**filters).aggregate(Sum("amount"))["amount__sum"]
      return paid

