# Generated by Django 3.0.7 on 2020-08-14 20:05

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutorial', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(null=True),
        ),
    ]