# Generated by Django 5.0.6 on 2024-06-25 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salary', '0004_salary_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='salary',
            name='week_start',
            field=models.DateField(default='2024-06-17'),
        ),
    ]
