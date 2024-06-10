from typing import Any
from .forms import SalaryForm
from django.views.generic import ListView
from .models import Salary


class SalaryListView(ListView):
    model = Salary
    template_name = 'salary/index.html'
    context_object_name = 'salaries'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = SalaryForm()
        return context

    def post(self, request, *args, **kwargs):
        form = SalaryForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)

            day_rate = 12.70
            sunday_rate = 13.20
            total_hours = 0
            total_minutes = 0

            day = form.cleaned_data['day']
            hours = form.cleaned_data['hours']
            minutes = form.cleaned_data['minutes']

            if hours == 0:
                hours = 1
            if minutes == 0:
                minutes == 1

            minutes /= 100

            if day == '7':
                total_hours = hours * sunday_rate
                total_minutes = minutes * sunday_rate

            else:
                total_hours = hours * day_rate
                total_minutes = minutes * day_rate

            total = total_hours + total_minutes

            instance.total_payment = total
            instance.save()

            print(form)

            # print(day, type(day))
            # print(hours, type(hours))
            # print(minutes, type(minutes))
            # print(f'{total:.2f}', type(total))

            return self.get(request, *args, **kwargs)

        context = self.get_context_data()
        context['form'] = form

        return self.render_to_response(context)
