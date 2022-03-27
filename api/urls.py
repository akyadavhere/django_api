from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.urls import path, include
from . import views

urlpatterns = [

    path('signup', views.Signup.as_view()),
    path('token', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('refresh', TokenRefreshView.as_view(), name="token_refresh"),
    path('verify', TokenVerifyView.as_view(), name="token_verify"),

    path("seller/", include([
        path("dashboard", views.Dashboard.as_view(), name="seller"),
        path('purchase', views.Purchase.as_view()),
        path('order', views.Order.as_view(), name="seller"),
        path('payment', views.Payment.as_view(), name="seller"),
        path('product', views.Product.as_view()),
        path('customer', views.Customer.as_view(), name="seller"),
        path('order/<int:pk>', views.Order.as_view()),
        path('payment/<int:pk>', views.Payment.as_view()),
        path('product/<int:pk>', views.Product.as_view()),
        path('customer/<int:pk>', views.Customer.as_view()),
    ])),

    path("customer/", include([
        path("dashboard", views.Dashboard.as_view(), name="customer"),
        path('order', views.Order.as_view(), name="customer"),
        path('payment', views.Payment.as_view(), name="customer"),
        path('seller', views.Customer.as_view(), name="customer"),
        path('order/<int:pk>', views.Order.as_view()),
    ])),
]