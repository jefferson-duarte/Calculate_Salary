from django.contrib import admin
from .models import Salary


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = [
        'day',
        'hours',
        'minutes',
        'total_payment',
        'user',
    ]
