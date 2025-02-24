# Generated by Django 5.1.6 on 2025-02-20 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TraceResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trace_id', models.TextField(blank=True, null=True)),
                ('id_number', models.TextField(blank=True, null=True)),
                ('cell_number', models.TextField(blank=True, null=True)),
                ('home1', models.TextField(blank=True, null=True)),
                ('work1', models.TextField(blank=True, null=True)),
                ('cell1', models.TextField(blank=True, null=True)),
                ('home2', models.TextField(blank=True, null=True)),
                ('work2', models.TextField(blank=True, null=True)),
                ('cell2', models.TextField(blank=True, null=True)),
                ('home3', models.TextField(blank=True, null=True)),
                ('work3', models.TextField(blank=True, null=True)),
                ('cell3', models.TextField(blank=True, null=True)),
                ('home4', models.TextField(blank=True, null=True)),
                ('work4', models.TextField(blank=True, null=True)),
                ('cell4', models.TextField(blank=True, null=True)),
                ('home5', models.TextField(blank=True, null=True)),
                ('work5', models.TextField(blank=True, null=True)),
                ('cell5', models.TextField(blank=True, null=True)),
                ('home6', models.TextField(blank=True, null=True)),
                ('work6', models.TextField(blank=True, null=True)),
                ('cell6', models.TextField(blank=True, null=True)),
                ('home7', models.TextField(blank=True, null=True)),
                ('work7', models.TextField(blank=True, null=True)),
                ('cell7', models.TextField(blank=True, null=True)),
                ('home8', models.TextField(blank=True, null=True)),
                ('work8', models.TextField(blank=True, null=True)),
                ('cell8', models.TextField(blank=True, null=True)),
                ('home9', models.TextField(blank=True, null=True)),
                ('work9', models.TextField(blank=True, null=True)),
                ('cell9', models.TextField(blank=True, null=True)),
                ('home10', models.TextField(blank=True, null=True)),
                ('work10', models.TextField(blank=True, null=True)),
                ('cell10', models.TextField(blank=True, null=True)),
                ('home11', models.TextField(blank=True, null=True)),
                ('work11', models.TextField(blank=True, null=True)),
                ('cell11', models.TextField(blank=True, null=True)),
                ('home12', models.TextField(blank=True, null=True)),
                ('work12', models.TextField(blank=True, null=True)),
                ('cell12', models.TextField(blank=True, null=True)),
                ('home13', models.TextField(blank=True, null=True)),
                ('work13', models.TextField(blank=True, null=True)),
                ('cell13', models.TextField(blank=True, null=True)),
                ('home14', models.TextField(blank=True, null=True)),
                ('work14', models.TextField(blank=True, null=True)),
                ('cell14', models.TextField(blank=True, null=True)),
                ('home15', models.TextField(blank=True, null=True)),
                ('work15', models.TextField(blank=True, null=True)),
                ('cell15', models.TextField(blank=True, null=True)),
                ('d_o_1', models.TextField(blank=True, null=True)),
                ('d_o_2', models.TextField(blank=True, null=True)),
                ('d_o_3', models.TextField(blank=True, null=True)),
                ('d_o_4', models.TextField(blank=True, null=True)),
                ('d_o_5', models.TextField(blank=True, null=True)),
                ('d_o_6', models.TextField(blank=True, null=True)),
                ('d_o_7', models.TextField(blank=True, null=True)),
                ('d_o_8', models.TextField(blank=True, null=True)),
                ('d_o_9', models.TextField(blank=True, null=True)),
                ('d_o_10', models.TextField(blank=True, null=True)),
                ('d_o_11', models.TextField(blank=True, null=True)),
                ('d_o_12', models.TextField(blank=True, null=True)),
                ('d_o_13', models.TextField(blank=True, null=True)),
                ('d_o_14', models.TextField(blank=True, null=True)),
                ('d_o_15', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Trace_result',
                'managed': False,
            },
        ),
    ]
