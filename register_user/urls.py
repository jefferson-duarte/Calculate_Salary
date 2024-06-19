from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path('create/', views.RegisterCreateView.as_view(), name='create'),
    path('login/', views.RegisterLoginView.as_view(), name='login'),
]
