from django.db import models
from django.contrib.auth.models import User


class Salary(models.Model):
    day_of_week = (
        ('1', 'Monday'),
        ('2', 'Tuesday'),
        ('3', 'Wednesday'),
        ('4', 'Thursday'),
        ('5', 'Friday'),
        ('6', 'Saturday'),
        ('7', 'Sunday'),
    )
    day = models.CharField(max_length=1, choices=day_of_week)
    value_hour = models.FloatField(default=0)
    hours = models.PositiveIntegerField()
    minutes = models.FloatField()
    total_payment = models.FloatField(default=0)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.day
