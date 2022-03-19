from django.urls import path
from .views import SignupView, UserView, ProductsView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('user/', UserView.as_view()),
    path('user/<int:pk>', UserView.as_view()),
    path('signup/', SignupView.as_view()),
    path('products/', ProductsView.as_view()),
    path('products/<int:pk>', ProductsView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('verify/', TokenVerifyView.as_view(), name="token_verify"),
]