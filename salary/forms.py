from django import forms
from .models import Salary


class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = [
            'day',
            'hours',
            'minutes',
        ]
