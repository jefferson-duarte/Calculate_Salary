from django.urls import reverse_lazy
from django.db.models import Sum
from typing import Any
from django.urls import reverse
from .forms import SalaryForm
from django.views.generic import ListView, CreateView, UpdateView
from .models import Salary
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class SalaryCreateView(LoginRequiredMixin, CreateView):
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

            instance.user = self.request.user

            # day_rate = 12.70
            # sunday_rate = 13.20

            value_hour = form.cleaned_data['value_hour']
            # day = form.cleaned_data['day']
            hours = form.cleaned_data['hours']
            minutes = form.cleaned_data['minutes']

            total_hours: int
            total_minutes: float
            minutes /= 100

            # if day == '7':
            #     total_hours = hours * sunday_rate
            #     total_minutes = minutes * sunday_rate
            #     total = total_hours + total_minutes
            #     instance.total_payment = total

            #     instance.save()
            #     messages.success(request, 'Salary added')

            #     return redirect('salary:create')

            total_hours = hours * value_hour
            total_minutes = minutes * value_hour
            total = total_hours + total_minutes
            instance.total_payment = total

            instance.save()
            messages.success(request, 'Salary added')

            return redirect('salary:create')

        return render(request, 'salary/create.html', {'form': form})


class SalaryListView(LoginRequiredMixin, ListView):
    model = Salary
    context_object_name = 'salaries'
    template_name = 'salary/list.html'
    ordering = 'day'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Salary.objects.filter(user=self.request.user)

        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        total_hours_no_sunday = (
            Salary.objects
            .filter(user=self.request.user)
            .filter(day__lt=int(7))
            .aggregate(total_sum=Sum('hours'))['total_sum']
        )

        total_minutes_no_sunday = (
            Salary.objects
            .filter(user=self.request.user)
            .filter(day__lt=int(7))
            .aggregate(total_sum=Sum('minutes'))['total_sum']
        )

        try:
            if total_minutes_no_sunday > 60:
                total_minutes_no_sunday /= 60
            else:
                total_minutes_no_sunday /= 100

            total_hours_week = total_hours_no_sunday + total_minutes_no_sunday
            context['total_hours_week'] = f'{total_hours_week:.2f}'.replace('.', ' : ')  # noqa:E501

        except TypeError:
            total_minutes_no_sunday = 0
            total_hours_week = 0
            context['total_hours_week'] = total_hours_week

        try:
            sunday_hours = (
                Salary.objects
                .filter(user=self.request.user)
                .get(day=7)
            )
            context['sunday_hours'] = sunday_hours.hours
            context['sunday_minutes'] = f'{sunday_hours.minutes:.0f}'

            sunday_hours.minutes /= 100
            total_minutes_no_sunday = round(total_minutes_no_sunday, 2)
            minutes = total_minutes_no_sunday + sunday_hours.minutes

            try:
                hours = total_hours_no_sunday + sunday_hours.hours
            except TypeError:
                total_hours_no_sunday = 0
                hours = total_hours_no_sunday + sunday_hours.hours

            total_hours = int(str(minutes + hours).split('.')[0])
            total_minutes = int(str(minutes + hours).split('.')[1])

            while True:
                if total_minutes > 60:
                    total_minutes -= 60
                    total_hours += 1
                else:
                    break

            total_hours = total_hours + (total_minutes / 100)

            context['total_hours'] = f'{total_hours:.2f}'.replace('.', ' : ')

        except Salary.DoesNotExist:
            context['sunday_hours'] = 0
            context['sunday_minutes'] = 0
            context['total_hours'] = f'{total_hours_week:.2f}'.replace('.', ' : ')  # noqa:E501

        total_payment_sum = (
            Salary.objects
            .filter(user=self.request.user)
            .aggregate(total_sum=Sum('total_payment'))['total_sum']
        )
        context['total_payment_sum'] = total_payment_sum or 0

        return context


class SalaryUpdateView(LoginRequiredMixin, UpdateView):
    model = Salary
    form_class = SalaryForm
    context_object_name = 'salaries'
    template_name = 'salary/update.html'
    success_url = reverse_lazy('salary:list')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Salary.objects.filter(user=self.request.user)

        return queryset

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user

        # day_rate = 12.70
        # sunday_rate = 13.20

        value_hour = form.cleaned_data['value_hour']
        # day = form.cleaned_data['day']
        hours = form.cleaned_data['hours']
        minutes = form.cleaned_data['minutes']

        if hours == 0:
            hours = 1
        if minutes == 0:
            minutes == 1

        minutes /= 100

        # if day == '7':
        #     total_hours = hours * sunday_rate
        #     total_minutes = minutes * sunday_rate
        # else:
        #     total_hours = hours * value_hour
        #     total_minutes = minutes * value_hour

        total_hours = hours * value_hour
        total_minutes = minutes * value_hour
        total = total_hours + total_minutes
        instance.total_payment = total
        instance.save()

        messages.success(self.request, 'Salary updated!')
        return super().form_valid(form)


def delete_salary(request, id):
    salary = Salary.objects.get(id=id)
    salary.delete()

    messages.success(request, 'Salary deleted!')

    return redirect('salary:list')
