# Generated by Django 3.1.2 on 2020-12-17 17:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('oes', '0025_auto_20201217_1013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam_detail',
            name='start_time',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
