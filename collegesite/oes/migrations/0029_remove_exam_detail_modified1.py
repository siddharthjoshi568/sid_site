# Generated by Django 3.1.2 on 2020-12-17 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oes', '0028_exam_detail_modified1'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam_detail',
            name='modified1',
        ),
    ]
