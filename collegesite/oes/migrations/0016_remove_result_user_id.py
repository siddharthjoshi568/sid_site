# Generated by Django 3.1.2 on 2020-12-08 09:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oes', '0015_result_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='user_id',
        ),
    ]
