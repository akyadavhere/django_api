from django.shortcuts import redirect
from django.contrib   import admin
from django.urls      import path, include
from api              import urls

urlpatterns = [
    path('', lambda _:redirect("api/")),
    path('admin/', admin.site.urls),
    path('api/', include(urls)),
]
