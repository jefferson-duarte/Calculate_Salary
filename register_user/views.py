from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView


class RegisterCreateView(CreateView):
    model = User
    form_class = RegisterForm
    context_object_name = 'register'
    template_name = 'register_user/pages/register.html'
    success_url = reverse_lazy('auth:login')


class RegisterLoginView(LoginView):
    template_name = 'register_user/pages/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('salary:list')
