# Generated by Django 3.1.2 on 2020-12-17 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oes', '0029_remove_exam_detail_modified1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exam_detail',
            name='start_time',
            field=models.DateTimeField(),
        ),
    ]