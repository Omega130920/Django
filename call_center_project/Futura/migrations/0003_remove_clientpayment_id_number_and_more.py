# Generated by Django 5.1.6 on 2025-03-05 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Futura', '0002_remove_call_day_of_month_remove_call_installments_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientpayment',
            name='ID_Number',
        ),
        migrations.AddField(
            model_name='clientpayment',
            name='id_number',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
