from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('salary.urls')),
    path('auth/', include('register_user.urls')),
]
