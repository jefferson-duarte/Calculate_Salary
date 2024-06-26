from django.urls import path
from . import views

app_name = 'salary'

urlpatterns = [
    path('', views.SalaryCreateView.as_view(), name='create'),
    path('salary/list/', views.SalaryListView.as_view(), name='list'),
    path('salary/delete/<int:id>/', views.delete_salary, name='delete'),
    path('salary/update/<int:pk>/', views.SalaryUpdateView.as_view(), name='update'),  # noqa: E501
]
