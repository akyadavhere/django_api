from rest_framework import serializers
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
   class Meta:
      model = models.Item
      fields = "__all__"
      read_only_fields = ["id"]