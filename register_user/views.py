from django.core.handlers.wsgi import WSGIRequest
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages


class RegisterCreateView(CreateView):
    model = User
    form_class = RegisterForm
    context_object_name = 'register'
    template_name = 'register_user/pages/register.html'
    success_url = reverse_lazy('auth:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Registration successful!')
        return response


class RegisterLoginView(LoginView):
    template_name = 'register_user/pages/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('salary:list')

    def form_invalid(self, form):
        messages.error(self.request, 'Username or password is incorrect')

        return super().form_invalid(form)

    def form_valid(self, form):
        messages.success(self.request, 'Login successful')

        return super().form_valid(form)


class RegisterLogoutView(LogoutView):
    next_page = reverse_lazy('auth:login')

    def post(self, request: WSGIRequest, *args: reverse_lazy, **kwargs: reverse_lazy) -> TemplateResponse:  # type: ignore # noqa:E501
        messages.success(self.request, 'Logout successful')

        return super().post(request, *args, **kwargs)
