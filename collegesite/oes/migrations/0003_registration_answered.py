# Generated by Django 3.1.2 on 2020-11-03 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oes', '0002_course_exam_detail_level_question_bank_registration_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='answered',
            field=models.IntegerField(default=0),
        ),
    ]
