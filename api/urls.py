from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('user/', views.User.as_view()),
    path('signup/', views.Signup.as_view()),
    path('product/', views.Products.as_view()),
    path('purchase/', views.Purchase.as_view()),
    path('user/<int:pk>', views.User.as_view()),
    path('product/<int:pk>', views.Products.as_view()),
    path('token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('verify/', TokenVerifyView.as_view(), name="token_verify"),
]