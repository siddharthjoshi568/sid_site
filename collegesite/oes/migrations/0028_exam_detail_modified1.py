# Generated by Django 3.1.2 on 2020-12-17 17:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('oes', '0027_auto_20201217_2257'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam_detail',
            name='modified1',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
