from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import get_user_model

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id","name","email","password"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        return get_user_model().objects.create_user(validated_data["name"], validated_data["email"], validated_data["password"])