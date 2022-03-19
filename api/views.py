from user.serializers             import CustomUserSerializer
from rest_framework.response      import Response
from django.contrib.auth          import get_user_model
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators    import api_view
from rest_framework.views         import APIView
from rest_framework.permissions   import IsAuthenticated
from . import serializers       
from . import models 


class SignupView(APIView):
    permission_classes = []

    @csrf_exempt
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"user created"})
        return Response(serializer.errors)


class ProductsView(APIView):
    permission_classes = []

    def get(self, request, pk=None):
        if pk:
            query_set = models.Products.objects.get(id=pk)
            serializer = serializers.Products(query_set)
        else:
            query_set = models.Products.objects.get(id=pk)
            serializer = serializers.Products(query_set, many=True)

        return Response(serializer.data)


    @csrf_exempt
    def post(self, request):
        serializer = serializers.Products(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"product created"})
        return Response(serializer.errors)






class UserView(APIView):
    permission_classes = []

    def get(self, request, pk=None):
        if pk:
            query_set = get_user_model().objects.filter(id=pk)
            serializer = CustomUserSerializer(query_set)

        else:
            query_set = get_user_model().objects.all()
            serializer = CustomUserSerializer(query_set, many=True)
        return Response(serializer.data)


    def delete(self, request, pk):
        get_user_model().objects.filter(id=pk).delete()
        return Response({"message":"user deleted"})





# {
#     "email": "customer's email",
#     "totol": "order total",
#     "items": [
#         {
#             "purchase": "purchase id",
#             "product": "product id",
#             "quantity": "product quantity"
#         }
#     ]
# }







