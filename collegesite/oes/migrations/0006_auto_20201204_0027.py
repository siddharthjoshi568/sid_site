# Generated by Django 3.1.2 on 2020-12-03 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oes', '0005_auto_20201204_0020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question_bank',
            name='answer',
            field=models.CharField(choices=[('option1', models.CharField(max_length=100)), ('option2', models.CharField(max_length=100)), ('option3', models.CharField(max_length=100)), ('option2', models.CharField(max_length=100))], max_length=100),
        ),
    ]
