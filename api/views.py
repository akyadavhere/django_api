from django.test import RequestFactory
from user.serializers             import CustomUserSerializer
from rest_framework.response      import Response
from django.contrib.auth          import get_user_model
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views         import APIView
from rest_framework.permissions   import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
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


class Products(APIView):

    def get(self, request, pk=None):
        if pk:
            query_set = models.Product.objects.get(seller=request.user.id, id=pk)
            serializer = serializers.ProductSerializer(query_set)
        else:
            print(request.user.id)
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
        models.Product.objects.get(id=pk).delete()
        return Response({"message":"product deleted"})


class Purchase(APIView):

    @csrf_exempt
    def post(self, request):
        request.data["seller"] = request.user.id
        request.data["customer"] = get_user_model().objects.get(email=request.data["customer"]).id

        serializer = serializers.SellerCustomerSerializer(data=request.data)
        if serializer.is_valid():
            seller_customer = serializer.save()
            request.data["seller_customer"] = seller_customer.id

            serializer = serializers.PurchaseSerializer(data=request.data)
            if serializer.is_valid():
                purchase = serializer.save()

                items = []
                for item in request.data["items"]:
                    item["purchase"] = purchase.id
                    serializer = serializers.ItemSerializer(data=item)
                    if serializer.is_valid():
                        items.append(serializers.ItemSerializer(serializer.save()).data)
                    else:
                        return Response(serializer.errors)

                return Response({
                    "message":"purchase added",
                    "response": [
                        serializers.SellerCustomerSerializer(seller_customer).data,
                        serializers.PurchaseSerializer(purchase).data,
                        items
                        ]
                    })
        
        return Response(serializer.errors)


class User(APIView):
    permission_classes = []

    def get(self, request, pk=None):
        if pk:
            query_set = get_user_model().objects.get(id=pk)
            serializer = CustomUserSerializer(query_set)

            # serializer = serializers.SellerCustomerSerializer(models.SellerCustomer.objects.get(id=pk))
        else:
            # query_set = get_user_model().objects.all()
            # serializer = CustomUserSerializer(query_set, many=True)

            serializer = serializers.ItemSerializer(models.Item.objects.all(),many=True)
        return Response(serializer.data)

    def delete(self, request, pk):
        models.SellerCustomer.objects.get(id=pk).delete()
        return Response({"message":"user deleted"})


