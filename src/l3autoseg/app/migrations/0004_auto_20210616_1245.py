# Generated by Django 3.2.3 on 2021-06-16 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20210616_1214'),
    ]

    operations = [
        migrations.AddField(
            model_name='datasetmodel',
            name='scores_file_path',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='datasetmodel',
            name='zip_file_path',
            field=models.CharField(max_length=1024, null=True),
        ),
    ]
