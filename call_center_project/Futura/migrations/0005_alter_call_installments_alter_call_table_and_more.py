# Generated by Django 5.1.6 on 2025-03-16 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Futura', '0004_call_day_of_month_call_installments_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='call',
            name='installments',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterModelTable(
            name='call',
            table='futura_call',
        ),
        migrations.AlterModelTable(
            name='clientlist',
            table='clientlist',
        ),
    ]
