from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('user/', views.User.as_view()),
    path('signup/', views.Signup.as_view()),
    path('dashboard/', views.Dashboard.as_view(), name="seller"),
    path('customerdashboard/', views.Dashboard.as_view(), name="customer"),
    path('product/', views.Product.as_view()),
    path('purchase/', views.Purchase.as_view()),
    path('order/', views.Order.as_view(), name="seller"),
    path('customerorder/', views.Order.as_view(), name="customer"),
    path('customerorder/<int:pk>', views.Order.as_view()),
    path('payment/', views.Payment.as_view(), name="seller"),
    path('customerpayment/', views.Payment.as_view(), name="customer"),
    path('customer/', views.Customer.as_view(), name="seller"),
    path('seller/', views.Customer.as_view(), name="customer"),
    path('user/<int:pk>', views.User.as_view()),
    path('product/<int:pk>', views.Product.as_view()),
    path('order/<int:pk>', views.Order.as_view()),
    path('payment/<int:pk>', views.Payment.as_view()),
    path('customer/<int:pk>', views.Customer.as_view()),
    path('token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('verify/', TokenVerifyView.as_view(), name="token_verify"),
]