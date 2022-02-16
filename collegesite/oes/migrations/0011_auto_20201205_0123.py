# Generated by Django 3.1.2 on 2020-12-04 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oes', '0010_auto_20201205_0007'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='no_ques_attempt',
            field=models.IntegerField(default=0, max_length=100),
        ),
        migrations.AddField(
            model_name='result',
            name='no_ques_right',
            field=models.IntegerField(default=0, max_length=100),
        ),
        migrations.AddField(
            model_name='result',
            name='no_ques_unattempt',
            field=models.IntegerField(default=0, max_length=100),
        ),
        migrations.AddField(
            model_name='result',
            name='no_ques_wrong',
            field=models.IntegerField(default=0, max_length=100),
        ),
        migrations.AddField(
            model_name='result',
            name='total_marks',
            field=models.IntegerField(default=0, max_length=100),
        ),
    ]
