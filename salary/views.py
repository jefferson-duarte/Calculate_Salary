from django.db.models import Sum
from typing import Any
from django.urls import reverse
from .forms import SalaryForm
from django.views.generic import ListView, CreateView
from .models import Salary
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages


class SalaryCreateView(CreateView):
    def get(self, request, *args, **kwargs):
        context = {
            'form': SalaryForm(),
            'form_action': reverse('salary:create'),
        }
        return render(request, 'salary/create.html', context)

    def post(self, request, *args, **kwargs):
        form = SalaryForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)

            day_rate = 12.70
            sunday_rate = 13.20

            day = form.cleaned_data['day']
            hours = form.cleaned_data['hours']
            minutes = form.cleaned_data['minutes']

            total_hours: int
            total_minutes: float
            minutes /= 100

            if day == '7':
                total_hours = hours * sunday_rate
                total_minutes = minutes * sunday_rate
                total = total_hours + total_minutes
                instance.total_payment = total

                instance.save()
                messages.success(request, 'Salary added')

                return redirect('salary:create')

            total_hours = hours * day_rate
            total_minutes = minutes * day_rate
            total = total_hours + total_minutes
            instance.total_payment = total

            instance.save()
            messages.success(request, 'Salary added')

            return redirect('salary:create')

        return render(request, 'salary/create.html', {'form': form})


class SalaryListView(ListView):
    model = Salary
    context_object_name = 'salaries'
    template_name = 'salary/list.html'
    ordering = 'day'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        total_payment_sum = (
            Salary.objects
            .aggregate(total_sum=Sum('total_payment'))['total_sum']
        )
        context['total_payment_sum'] = total_payment_sum or 0

        return context


def delete_salary(request, id):
    salary = Salary.objects.get(id=id)
    salary.delete()

    messages.success(request, 'Salary deleted!')

    return redirect('salary:list')


def edit_salary(request, id):
    salary = get_object_or_404(
        Salary,
        id=id,
    )

    form_action = reverse('salary:edit', args=(id,))

    if request.method == 'POST':
        form = SalaryForm(request.POST, instance=salary)

        context = {
            'form': form,
            'form_action': form_action,
        }

        if form.is_valid():
            salary.save()

            return redirect(
                'salary:edit',
                id=salary.id
            )

        return render(request, 'salary/index.html', context)

    form = SalaryForm(instance=salary)

    context = {
        'form': form,
    }

    return render(
        request,
        'salary/list.html',
        context
    )
