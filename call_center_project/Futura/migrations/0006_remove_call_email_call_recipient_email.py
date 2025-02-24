# Generated by Django 5.1.6 on 2025-02-23 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Futura', '0005_call_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='call',
            name='Email',
        ),
        migrations.AddField(
            model_name='call',
            name='recipient_email',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
