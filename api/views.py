from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from django.db.models import Sum
from django.urls import resolve

from user.serializers import CustomUserSerializer
from django.contrib.auth import get_user_model
from . import serializers    
from . import models

from .request_user import get_user

from django.conf import settings
from django.core.mail import send_mail


class Signup(APIView):
    authentication_classes = []
    permission_classes = []

    @csrf_exempt
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"user created"})
        return Response(serializer.errors)


class Product(APIView):
    def get(self, request, pk=None):
        if pk:
            query_set = models.Product.objects.get(seller=get_user(request).id, id=pk)
            serializer = serializers.ProductSerializer(query_set)
        else:
            query_set = models.Product.objects.filter(seller=get_user(request).id)
            serializer = serializers.ProductSerializer(query_set, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request):
        request.data["seller"] = get_user(request).id
        serializer = serializers.ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer = serializers.ProductSerializer(serializer.save())
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk):
        product = models.Product.objects.get(id=pk)
        if models.Item.objects.filter(product=product).exists():
            product.seller = None
            product.save()
        else:
            product.delete()
        return Response({"message":"product deleted"})


class Purchase(APIView):
    @csrf_exempt
    def post(self, request):
        request.data["seller"] = get_user(request).id
        customer_email = request.data["customer"]
        request.data["customer"] = get_user_model().objects.get(email=request.data["customer"]).id
        
        sub = "New order added - Shoprecords"
        msg = f"A new order added to your shoprecords's account by seller ({get_user(request).email}) "

        if request.data["seller"] == request.data["customer"]:
            return Response(status=HTTP_400_BAD_REQUEST)

        serializer = serializers.SellerCustomerSerializer(data=request.data)
        if serializer.is_valid():
            request.data["seller_customer"] = serializer.save().id

            serializer = serializers.PurchaseSerializer(data=request.data)
            if serializer.is_valid():
                purchase = serializer.save()

                for item in request.data["items"]:
                    item["purchase"] = purchase.id
                    serializer = serializers.ItemSerializer(data=item)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        return Response(serializer.errors)
                send_mail(sub, msg, settings.EMAIL_HOST_USER, [customer_email], fail_silently=True)
                return Response({"message":"purchase added"})
        return Response(serializer.errors)


class Payment(APIView):
    def get(self, request):
        current_url = resolve(request.path_info).url_name
        filters = {f"seller_customer__{current_url}": get_user(request).id}
        query_set = models.Payment.objects.filter(**filters).order_by("-datetime")
        serializer = serializers.PaymentSerializer(query_set, many=True, context={"current_url":current_url})
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request):
        request.data["seller"] = get_user(request).id
        request.data["customer"] = get_user_model().objects.get(email=request.data["customer"]).id

        if request.data["seller"] == request.data["customer"]:
            return Response(status=HTTP_400_BAD_REQUEST)
        
        serializer = serializers.SellerCustomerSerializer(data=request.data)
        if serializer.is_valid():
            request.data["seller_customer"] = serializer.save().id

            serializer = serializers.PaymentSerializer(data=request.data)
            if serializer.is_valid():
                payment = serializer.save()
                serializer = serializers.PaymentSerializer(payment)
                return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk):
        models.Payment.objects.get(id=pk).delete()
        return Response({"message":"user deleted"})


class Customer(APIView):
    def get(self, request):
        current_url = resolve(request.path_info).url_name
        if current_url == "seller":
            filters = {"user_as_customer__seller": get_user(request).id}
        else:
            filters = {"user_as_seller__customer": get_user(request).id}
        query_set = get_user_model().objects.filter(**filters)
        serializer = serializers.CustomerSerializer(query_set, context={"user":get_user(request), "current_url":current_url}, many=True)
        return Response(serializer.data)

    def delete(self, request, pk):
        models.SellerCustomer.objects.get(seller=get_user(request).id, customer=pk).delete()
        return Response({"message":"user deleted"}) 


class Dashboard(APIView):
    def get(sef, request):
        current_url = resolve(request.path_info).url_name
        filters = {f"seller_customer__{current_url}": get_user(request).id}
        total = models.Purchase.objects.filter(**filters, status=True).aggregate(Sum("amount"))["amount__sum"]
        paid = models.Payment.objects.filter(**filters).aggregate(Sum("amount"))["amount__sum"]
        query_set = models.Purchase.objects.filter(**filters, status=True).values("datetime__date").annotate(total=Sum("amount")).order_by("datetime__date")
        return Response({"total": total,"paid": paid,"graph": query_set})


class Order(APIView):
    def get(self, request):
        current_url = resolve(request.path_info).url_name
        filters = {f"seller_customer__{current_url}": get_user(request).id}
        query_set = models.Purchase.objects.filter(**filters).order_by("-datetime")
        serializer = serializers.OrderSerializer(query_set, many=True, context={"current_url":current_url})
        return Response(serializer.data)

    def patch(self, request, pk):
        purchase = models.Purchase.objects.get(id=pk)
        purchase.status = not purchase.status
        purchase.save()
        return Response({"message":"status updated"})

    def delete(self, request, pk):
        models.Purchase.objects.get(id=pk).delete()
        return Response({"message":"order deleted"})
