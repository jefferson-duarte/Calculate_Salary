from django.db import models


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
    # TODO: add input for day_rate and sunday_rate
    hours = models.PositiveIntegerField()
    minutes = models.FloatField()
    total_payment = models.FloatField(default=0)

    def __str__(self):
        return self.day
