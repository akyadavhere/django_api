from optparse import Values
from statistics import variance
from user.serializers             import CustomUserSerializer
from rest_framework.response      import Response
from django.contrib.auth          import get_user_model
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views         import APIView
from django.db.models import Sum, Count
from . import serializers       
from . import models 


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
            query_set = models.Product.objects.get(seller=request.user.id, id=pk)
            serializer = serializers.ProductSerializer(query_set)
        else:
            query_set = models.Product.objects.filter(seller=request.user.id)
            serializer = serializers.ProductSerializer(query_set, many=True)

        return Response(serializer.data)

    @csrf_exempt
    def post(self, request):
        request.data["seller"] = request.user.id
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
        request.data["seller"] = request.user.id
        request.data["customer"] = get_user_model().objects.get(email=request.data["customer"]).id

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

                return Response({"message":"purchase added"})
        
        return Response(serializer.errors)


class Order(APIView):
    
    def get(self, request):
        query_set = models.Purchase.objects.filter(seller_customer__seller=request.user).order_by("-datetime")
        serializer = serializers.OrderSerializer(query_set, many=True)
        return Response(serializer.data)

    def delete(self, request, pk):
        models.Purchase.objects.get(id=pk).delete()
        return Response({"message":"order deleted"})


class Payment(APIView):

    def get(self, request):
        query_set = models.Payment.objects.filter(seller_customer__seller=request.user.id).order_by("-datetime")
        serializer = serializers.PaymentSerializer(query_set, many=True)
        return Response(serializer.data)

    @csrf_exempt
    def post(self, request):
        request.data["seller"] = request.user.id
        request.data["customer"] = get_user_model().objects.get(email=request.data["customer"]).id
        
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
        query_set = get_user_model().objects.filter(user_as_customer__seller=request.user)
        serializer = serializers.CustomerSerializer(query_set, context={"user":request.user}, many=True)
        return Response(serializer.data)

    def delete(self, request, pk):
        models.SellerCustomer.objects.get(seller=request.user, customer=pk).delete()
        return Response({"message":"user deleted"}) 


class Dashboard(APIView):
    
    def get(sef, request):
        total = models.Purchase.objects.filter(seller_customer__seller=request.user).aggregate(Sum("amount"))["amount__sum"]
        paid = models.Payment.objects.filter(seller_customer__seller=request.user).aggregate(Sum("amount"))["amount__sum"]
        query_set = models.Purchase.objects.filter(seller_customer__seller=request.user).values("datetime__date").annotate(total=Sum("amount")).order_by()
        return Response({
            "total": total,
            "paid": paid,
            "graph": query_set
            })


class User(APIView):
    permission_classes = []

    def get(self, request, pk=None):
        if pk:
            query_set = models.Product.objects.get(id=pk)
            serializer = serializers.ProductSerializer(query_set)

            # serializer = serializers.SellerCustomerSerializer(models.SellerCustomer.objects.get(id=pk))
        else:
            query_set = get_user_model().objects.all()
            serializer = CustomUserSerializer(query_set, many=True)

            # serializer = serializers.ProductSerializer(models.Product.objects.all(),many=True)
        return Response(serializer.data)

    def delete(self, request, pk):
        models.Product.objects.get(id=pk).delete()
        return Response({"message":"user deleted"})


