# Generated by Django 3.2.3 on 2021-06-16 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210604_0809'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagemodel',
            name='json_file_name',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='imagemodel',
            name='json_file_path',
            field=models.CharField(max_length=1024, null=True),
        ),
    ]
